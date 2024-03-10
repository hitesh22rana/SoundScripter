# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

import io
import re
import zipfile
from io import BytesIO
from pathlib import Path

import psutil
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.background_tasks.transcription import (
    generate_transcription,
    terminate_transcription,
)
from app.config import settings
from app.models import FilesModel, TranscriptionsModel
from app.schemas import (
    DataResponse,
    TranscriptionBackgroundJobPayloadSchema,
    TranscriptionSchema,
)
from app.utils.file_manager import file_manager
from app.utils.responses import OK
from app.utils.shared import Language, Priority, Sort, Status


class TranscriptionService:
    local_storage_base_path: str = settings.local_storage_base_path

    image: str = "transcription-service"
    container_base_path: str = "home/data"
    model: str = "ggml-small.en.bin"
    arcname: str = "transcription"

    def __init__(
        self,
        session: Session,
    ) -> None | HTTPException:
        """
        Transcription Service
        :param -> session: Session
        :return -> None | HTTPException
        """

        self.session: Session = session

    @classmethod
    def _get_container_config(
        cls,
        file_id: str,
    ) -> dict:
        """
        Generate docker container config
        :return -> dict
        """

        bind_volume_path: str = cls.local_storage_base_path + "/" + file_id

        container_config: dict = {
            "image": cls.image,
            "volumes": {
                bind_volume_path: {
                    "bind": f"/{cls.container_base_path}",
                    "mode": "rw",
                }
            },
        }

        return container_config

    @classmethod
    def _get_file_path(
        cls,
        file_name,
    ) -> str:
        """
        Generate relative file path for the audio file
        :return -> str
        """

        return f"/{cls.container_base_path}/{file_name}.wav"

    @classmethod
    def _get_output_folder_path(
        cls,
        file_name: str,
    ) -> str:
        """
        Generate relative output folder path for the audio file
        :return -> str
        """

        return f"/{cls.container_base_path}/{file_name}"

    @classmethod
    def _get_model_path(cls) -> str:
        """
        Generate relative model path
        :return -> str
        """

        return f"/root/models/{cls.model}"

    @classmethod
    def _get_thread_count(
        cls,
        priority: Priority,
    ) -> int:
        """
        Generate thread count based on priority
        :param -> priority: Priority
        :return -> int
        """

        threads_count: int = psutil.cpu_count(logical=True)

        if priority == Priority.LOW:
            return max(threads_count // 4, 1)

        elif priority == Priority.MEDIUM:
            return max(threads_count // 2, 1)

        return max(threads_count // 2 - 1, 1)

    @classmethod
    def _get_spoken_language(
        cls,
        langauge: Language,
    ) -> str:
        """
        Generate spoken language
        :param -> langauge: Language
        :return -> str
        """

        return langauge.value

    @classmethod
    def _get_command(
        cls,
        langauge: Language,
        priority: Priority,
        file_name: str,
    ) -> str:
        """
        Generate docker command
        :param -> langauge: Language, priority: Priority
        :return -> str
        """

        # TODO:- Add support for multiple languages
        # TODO:- Add support for multiple models

        return f"whisper -t {cls._get_thread_count(priority=priority)} -l {cls._get_spoken_language(langauge=langauge)} -m {cls._get_model_path()} -f {cls._get_file_path(file_name=file_name)} -osrt -of {cls._get_output_folder_path(file_name=file_name)}"

    @classmethod
    async def _generate_zip(
        cls,
        arcname: str,
        files: list[Path],
    ) -> BytesIO | Exception:
        """
        Generate zip file
        :param -> files: list[Path]
        :return -> BytesIO | Exception
        """

        try:
            zip_stream = io.BytesIO()

            with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    zipf.write(file, arcname=arcname + file.suffix)

            return zip_stream

        except Exception as e:
            raise e

    async def list(
        self,
        limit: int,
        offset: int,
        sort: Sort,
    ) -> list[DataResponse.response] | HTTPException:
        """
        List transcriptions
        :param -> limit: int, offset: int, sort: Sort
        :return -> list[DataResponse.response] | HTTPException
        """

        try:
            results: list = (
                self.session.query(FilesModel, TranscriptionsModel)
                .outerjoin(FilesModel, FilesModel.id == TranscriptionsModel.file_id)
                .order_by(
                    FilesModel.created_at.asc()
                    if sort == Sort.ASC
                    else FilesModel.created_at.desc()
                )
                .limit(limit)
                .offset(offset)
                .all()
            )

            self.session.close()

            data: list[DataResponse.response] = [
                DataResponse(row).response() for row in results
            ]

            return OK(
                content={
                    "detail": "Success: Transcriptions list fetched successfully",
                    "data": data,
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: List service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def transcribe(
        self,
        transcription_details: TranscriptionSchema,
    ) -> OK | HTTPException:
        """
        Add the transcription request in the task queue for further processing
        :param -> transcription_details: TranscriptionSchema
        :return -> OK | HTTPException
        """

        file_id: str = transcription_details.file_id
        language: Language = transcription_details.language
        priority: Priority = transcription_details.priority

        try:
            file: FilesModel = (
                self.session.query(FilesModel)
                .filter(FilesModel.id == str(file_id))
                .first()
            )

            if file is None:
                raise FileNotFoundError()

            # Additional validation if file is already transcribed or is in process, return HTTPException stating file is already in process
            if file.status == Status.ERROR:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: File was not uploaded successfully",
                    }
                )

            elif file.status != Status.DONE:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: File is not yet uploaded",
                    }
                )

            # Additional validation for the file, could be removed
            if not file_manager.validate_file_path(file.path):
                raise FileNotFoundError()

            if file.transcription is not None:
                if file.transcription.status == Status.DONE:
                    raise Exception(
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Error: File is already transcribed",
                        }
                    )

                elif (
                    file.transcription.status == Status.PROCESSING
                    or file.transcription.status == Status.QUEUED
                ):
                    raise Exception(
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Error: File is already processing",
                        }
                    )

            # Get the currently executing high priority tasks count
            currently_executing_tasks: list[TranscriptionsModel] = (
                self.session.query(TranscriptionsModel)
                .filter(TranscriptionsModel.status == Status.PROCESSING)
                .order_by(None)
                .all()
            )

            high_priority_tasks_count: int = 0
            medium_priority_tasks_count: int = 0
            low_priority_tasks_count: int = 0

            for task in currently_executing_tasks:
                if task.priority == Priority.HIGH:
                    high_priority_tasks_count += 1

                elif task.priority == Priority.MEDIUM:
                    medium_priority_tasks_count += 1

                elif task.priority == Priority.LOW:
                    low_priority_tasks_count += 1

            if high_priority_tasks_count == 1:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: 1 high priority tasks in process",
                    }
                )

            elif medium_priority_tasks_count == 2:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: 2 medium priority tasks in process",
                    }
                )

            elif medium_priority_tasks_count == 1 and low_priority_tasks_count == 2:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: 1 medium priority task and 2 low priority tasks in process",
                    }
                )

            elif low_priority_tasks_count == 4:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": f"Error: 4 low priority tasks in process, {priority} priority tasks can't be executed at this time",
                    }
                )

            total_tasks_count: int = (
                high_priority_tasks_count
                + medium_priority_tasks_count
                + low_priority_tasks_count
            )

            if priority == Priority.HIGH and total_tasks_count != 0:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": f"Error: {total_tasks_count} tasks in process, high priority tasks can't be executed at this time",
                    }
                )

            elif priority == Priority.MEDIUM and low_priority_tasks_count > 2:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": f"Error: {low_priority_tasks_count} low priority tasks in process, medium priority tasks can't be executed at this time",
                    }
                )

            elif priority == Priority.LOW and low_priority_tasks_count > 3:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": f"Error: {low_priority_tasks_count} low priority tasks in process, low priority tasks can't be executed at this time",
                    }
                )

            file_names: list[str] = file_manager.get_transcription_input_files(
                file_id=file_id
            )

            if priority == Priority.HIGH:
                file_names = [
                    file_name for file_name in file_names if re.search("\d", file_name)
                ]
            else:
                file_names = [
                    file_name
                    for file_name in file_names
                    if not re.search("\d", file_name)
                ]

            data = TranscriptionBackgroundJobPayloadSchema(
                id=file_id,
                container_config=self._get_container_config(file_id=file_id),
                detach=False,
                remove=True,
                commands=[
                    self._get_command(
                        langauge=language,
                        priority=priority,
                        file_name=file_name,
                    )
                    for file_name in file_names
                ],
            ).model_dump()

            transcription_model: TranscriptionsModel = TranscriptionsModel(
                file_id=file_id, language=language, priority=priority
            )

            self.session.add(transcription_model)
            self.session.commit()
            self.session.refresh(transcription_model)
            self.session.close()

            task = generate_transcription.delay(data=data)

            return OK(
                content={
                    "task_id": task.id,
                    "detail": "Success: File is added to transcription queue",
                }
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            ) from e

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Transcription service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def download(
        self,
        file_id: str,
    ) -> StreamingResponse | HTTPException:
        """
        Download file
        :param -> file_id: str
        :return -> StreamingResponse | HTTPException
        """

        try:
            transcription: TranscriptionsModel = (
                self.session.query(TranscriptionsModel)
                .filter_by(file_id=file_id)
                .first()
            )

            if not transcription:
                raise FileNotFoundError()

            if transcription.status != Status.DONE:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: Transcription is not completed yet",
                    }
                )

            output_directory: str = (
                file_manager.get_folder_path(file_id=file_id) + "/transcriptions"
            )

            output_files: list[Path] = file_manager.get_generated_transcriptions(
                output_directory
            )

            # Generate the ZIP archive asynchronously
            zip_stream: BytesIO = await self._generate_zip(
                arcname=self.arcname, files=output_files
            )

            # Serve the ZIP archive as a downloadable file
            return StreamingResponse(
                io.BytesIO(zip_stream.getvalue()),
                media_type="application/zip",
                headers={
                    "Content-Disposition": f"attachment; filename={transcription.file.name}.zip",
                },
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: File not found",
            ) from e

        except Exception as e:
            print(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Download service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def terminate(self, file_id: str) -> OK | HTTPException:
        """
        Terminate running transcription
        :param -> file_id: str
        :return -> OK | HTTPException
        """

        try:
            transcription: TranscriptionsModel = (
                self.session.query(TranscriptionsModel)
                .filter_by(file_id=file_id)
                .first()
            )

            if not transcription or transcription.status != Status.PROCESSING:
                raise Exception(
                    {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "detail": "Error: Transcription is not in process",
                    }
                )

            task = terminate_transcription.delay(
                file_id=file_id, container_ids=transcription.task_ids
            )

            return OK(
                content={
                    "task_id": task.id,
                    "detail": "Success: Transcription task is cancelled",
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Termination service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

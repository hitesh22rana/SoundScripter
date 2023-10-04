# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.background_tasks.transcription import generate_transcriptions
from app.config import settings
from app.models import FilesModel, TranscriptionsModel
from app.schemas import (
    DataResponse,
    TranscriptionBackgroundJobPayloadSchema,
    TranscriptionSchema,
)
from app.utils.file_manager import FileManager
from app.utils.responses import OK
from app.utils.shared import Sort, Status


class TranscriptionService:
    local_storage_base_path: str = settings.local_storage_base_path

    image: str = "transcription-service"
    container_base_path: str = "home/data"

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

    def _get_container_config(self, file_id: str) -> dict:
        """
        Generate docker container config
        :return -> dict
        """

        bind_volume_path: str = (
            TranscriptionService.local_storage_base_path + "/" + file_id
        )

        container_config: dict = {
            "image": TranscriptionService.image,
            "volumes": {
                bind_volume_path: {
                    "bind": f"/{TranscriptionService.container_base_path}",
                    "mode": "rw",
                }
            },
        }

        return container_config

    def _get_file_path(self) -> str:
        """
        Generate relative file path for the audio file
        :return -> str
        """

        return f"/{TranscriptionService.container_base_path}/file.wav"

    def _get_output_folder_path(self) -> str:
        """
        Generate relative output folder path for the audio file
        :return -> str
        """

        return f"/{TranscriptionService.container_base_path}/transcriptions"

    def _get_model_path(self, model: str) -> str:
        """
        Generate relative model path
        :return -> str
        """

        return f"/root/models/{model}"

    async def list(
        self, limit: int, offset: int, sort: Sort
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
                {
                    "detail": "Success: Transcriptions list fetched successfully",
                    "data": data,
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: List service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def transcribe(
        self, transcription_details: TranscriptionSchema
    ) -> OK | HTTPException:
        """
        Add the transcription request in the task queue for further processing
        :params -> transcription_details: TranscriptionSchema
        :return -> OK | HTTPException
        """

        file_id: str = transcription_details.file_id
        language: str = transcription_details.language

        # TODO:- Add support for multiple languages
        if language != "English":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Currently only English is supported",
            )

        model: str = "ggml-small.en-q5_1.bin"

        file_manager: FileManager = FileManager()

        try:
            file: FilesModel = (
                self.session.query(FilesModel)
                .filter(FilesModel.id == str(file_id))
                .first()
            )

            # Additional validation for the file, could be removed
            file_path: str = file_manager.get_file_path_from_id(file_id=file_id)

            if file is None or file_path != file.path:
                raise FileNotFoundError()

            # Additional validation if file is already transcribed or is in process, return HTTPException stating file is already in process
            if file is not None and file.transcription is not None:
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

            data: dict = TranscriptionBackgroundJobPayloadSchema(
                id=file_id,
                container_config=self._get_container_config(file_id=file_id),
                detach=False,
                remove=True,
                command=f"whisper -t 2 -m {self._get_model_path(model=model)} -f {self._get_file_path()} -osrt -ovtt -of {self._get_output_folder_path()}",
            ).model_dump()

            transcription_model: TranscriptionsModel = TranscriptionsModel(
                file_id=file_id
            )

            self.session.add(transcription_model)
            self.session.commit()
            self.session.refresh(transcription_model)
            self.session.close()

            task = generate_transcriptions.delay(data=data)

            return OK(
                {
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

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

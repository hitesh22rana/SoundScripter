# Purpose: File Service for handling files related operations.
# Path: backend\app\services\files.py


import asyncio

import aiofiles
from fastapi import File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.background_tasks.optimization import (
    change_audio_sample_rate,
    convert_video_to_audio,
)
from app.models import FilesModel, TranscriptionsModel
from app.schemas import ConversionBackgroundJobPayloadSchema, FileResponse
from app.utils.file_manager import file_manager
from app.utils.responses import OK, Accepted
from app.utils.shared import Sort, Type


class FileService:
    def __init__(self, session: Session) -> None:
        """
        File Service
        :param -> session: Session = None
        :return -> None
        """

        self.session: Session = session
        self.upload_data_chunks_queue: asyncio.Queue = asyncio.Queue()

    async def _async_file_reader(self, file: UploadFile = File(...)):
        while True:
            chunk = await file.read(1024 * 1024 * 100)
            if not chunk:
                break
            await self.upload_data_chunks_queue.put(chunk)

    async def _async_file_writer(self, file_path: str):
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await self.upload_data_chunks_queue.get()
                if not chunk:
                    break
                await f.write(chunk)

    async def upload(
        self, name: str, file: UploadFile = File(...)
    ) -> None | HTTPException:
        """
        Upload file
        :param -> name: str, file: UploadFile = File(...)
        :return -> Accepted | HTTPException
        """

        file_id: str = file_manager.get_unique_file_id()
        file_extension: str = file_manager.get_file_extension(file_name=file.filename)

        if (
            not file_manager.validate_payload_file_type(file.content_type)
            or not file_extension
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Invalid file type",
            )

        file_path: str = file_manager.generate_file_path(
            file_name=file_id, file_extension=file_extension
        )

        try:
            # Start file reader and writer tasks
            async_reader_task = asyncio.create_task(self._async_file_reader(file))
            async_writer_task = asyncio.create_task(self._async_file_writer(file_path))

            # Wait for the reader task to complete and signal the writer task
            await asyncio.gather(async_reader_task)
            await self.upload_data_chunks_queue.put(None)

            # Wait for the writer task to complete
            await asyncio.gather(async_writer_task)

            # Create a FilesModel instance to save the file details in the database
            file_model: FilesModel = FilesModel(id=file_id, name=name, path=file_path)

            data: dict = (
                ConversionBackgroundJobPayloadSchema(
                    id=file_id,
                    current_path=file_path,
                    current_format=file_extension[1:],
                    sample_rate=16000,  # 16 kHz
                    output_path=file_path.replace(file_extension[1:], "wav"),
                    output_format="wav",
                    delete_original_file=True,
                    parts_count=2,
                )
            ).model_dump()

            if file_manager.is_audio_file_extension(file_extension[1:]):
                self.session.add(file_model)
                self.session.commit()
                self.session.refresh(file_model)
                self.session.close()

                change_audio_sample_rate.delay(data=data)

            elif file_manager.is_video_file_extension(file_extension[1:]):
                # Update default Audio type to Video
                file_model.type = Type.VIDEO
                self.session.add(file_model)
                self.session.commit()
                self.session.refresh(file_model)
                self.session.close()

                convert_video_to_audio.delay(data=data)

            return Accepted(
                content={
                    "file_id": file_id,
                    "detail": "Success: File uploaded successfully",
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Upload service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def list(
        self, limit: int, offset: int, sort: Sort
    ) -> list[FileResponse.response] | HTTPException:
        """
        List files
        :param -> limit: int, offset: int, sort: Sort
        :return -> list[FileResponse.response] | HTTPException
        """

        try:
            results: list[FilesModel] = (
                self.session.query(FilesModel)
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

            data: list[FileResponse.response] = [
                FileResponse(row).response() for row in results
            ]

            return OK(
                content={
                    "detail": "Success: Files list fetched successfully",
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

    async def delete(self, file_id: str) -> None | HTTPException:
        """
        Delete file
        :param -> file_id: str
        :return -> None | HTTPException
        """

        try:
            self.session.query(TranscriptionsModel).filter_by(file_id=file_id).delete(
                synchronize_session=False
            )
            self.session.query(FilesModel).filter_by(id=file_id).delete(
                synchronize_session=False
            )

            self.session.commit()
            self.session.close()

            folder_path = file_manager.get_folder_path(file_id=file_id)
            file_manager.delete_folder(folder_path=folder_path)

            return Accepted(
                content={
                    "file_id": file_id,
                    "detail": "Success: File deleted successfully",
                }
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: File not found",
            ) from e

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Delete service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

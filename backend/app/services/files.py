# Purpose: File Service for handling files related operations.
# Path: backend\app\services\files.py


import aiofiles
from fastapi import File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.background_tasks.conversion import (
    change_audio_sample_rate,
    convert_video_to_audio,
)
from app.models import FilesModel, TranscriptionsModel
from app.schemas import ConversionBackgroundJobPayloadSchema, FileResponse
from app.utils.file_manager import FileManager
from app.utils.responses import OK, Accepted
from app.utils.shared import Sort, Type


class FileService(FileManager):
    def __init__(self, session: Session) -> None:
        """
        File Service
        :param -> session: Session = None
        :return -> None
        """

        super().__init__()

        self.session: Session = session

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
                {"detail": "Success: Files list fetched successfully", "data": data}
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: List service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def upload(
        self, name: str, file: UploadFile = File(...)
    ) -> None | HTTPException:
        """
        Upload file
        :param -> name: str, file: UploadFile = File(...)
        :return -> Accepted | HTTPException
        """

        file_id: str = self.get_unique_file_id()
        file_extension: str = self.get_file_extension(file_name=file.filename)

        if not self.validate_payload_file_type(file.content_type) or not file_extension:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Invalid file type",
            )

        file_path: str = self.generate_file_path(
            file_name=file_id, file_extension=file_extension
        )

        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(
                    self.chunk_size_bytes * self.chunk_size_bytes
                ):
                    await f.write(chunk)

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
                )
            ).model_dump()

            if self.is_audio_file_extension(file_extension[1:]):
                self.session.add(file_model)
                self.session.commit()
                self.session.refresh(file_model)
                self.session.close()

                change_audio_sample_rate.delay(data=data)

            elif self.is_video_file_extension(file_extension[1:]):
                # Update default Audio type to Video
                file_model.type = Type.VIDEO
                self.session.add(file_model)
                self.session.commit()
                self.session.refresh(file_model)
                self.session.close()

                convert_video_to_audio.delay(data=data)

            return Accepted(
                {
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

            folder_path = self.get_folder_path(file_id=file_id)
            self.delete_folder(folder_path=folder_path)

            return Accepted(
                {
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

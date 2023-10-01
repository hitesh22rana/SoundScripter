# Purpose: File Service for handling files related operations.
# Path: backend\app\services\files.py

import io
import zipfile
from io import BytesIO
from pathlib import Path

import aiofiles
from fastapi import File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.background_tasks.conversion import (
    change_audio_sample_rate,
    convert_video_to_audio,
)
from app.models import FilesModel
from app.schemas.files import FileResponse
from app.utils.file_manager import FileManager
from app.utils.responses import OK, Accepted
from app.utils.shared import Sort, Type


class FileService(FileManager):
    arcname: str = "transcription"

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
    ) -> list[dict] | HTTPException:
        """
        List files
        :param -> limit: int, offset: int, sort: Sort
        :return -> list[dict] | HTTPException
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

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def upload(self, file: UploadFile = File(...)) -> None | HTTPException:
        """
        Upload file
        :param -> file: UploadFile = File(...)
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
            file_model = FilesModel(id=file_id, path=file_path)

            if self.is_audio_file_extension(file_extension[1:]):
                change_audio_sample_rate.delay(
                    data={
                        "file_id": file_id,
                        "audio_path": file_path,
                        "audio_format": file_extension[1:],
                        "sample_rate": 16000,  # 16 kHz
                        "output_path": file_path.replace(file_extension[1:], "wav"),
                        "output_format": "wav",
                        "delete_original_file": True,
                    }
                )

            elif self.is_video_file_extension(file_extension[1:]):
                # Update default Audio type to Video
                file_model.type = Type.VIDEO

                convert_video_to_audio.delay(
                    data={
                        "file_id": file_id,
                        "video_path": file_path,
                        "video_extension": file_extension[1:],
                        "audio_format": "wav",
                        "delete_original_file": True,
                    }
                )

            self.session.add(file_model)
            self.session.commit()
            self.session.refresh(file_model)
            self.session.close()

            return Accepted(
                {
                    "file_id": file_id,
                    "detail": "Success: File uploaded successfully",
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Upload service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

    async def download(self, file_id: str) -> StreamingResponse | HTTPException:
        """
        Download file
        :param -> file_id: str
        :return -> StreamingResponse | HTTPException
        """

        # TODO:- Check database if transcriptions are generated or not

        try:
            files: list[Path] = self.get_transcription_files(file_id=file_id)

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: File not found",
            ) from e

        try:
            # Generate the ZIP archive asynchronously
            zip_stream: BytesIO = await self.generate_zip(
                arcname=FileService.arcname, files=files
            )

            # Serve the ZIP archive as a downloadable file
            return StreamingResponse(
                io.BytesIO(zip_stream.getvalue()),
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={file_id}.zip"},
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Download service is not available"

            if isinstance(e.args[0], dict):
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
            self.session.query(FilesModel).filter_by(id=file_id).delete()
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

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

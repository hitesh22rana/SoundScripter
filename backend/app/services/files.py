# Purpose: File Service for handling files related operations.
# Path: backend\app\services\files.py

import io
import zipfile
from io import BytesIO
from pathlib import Path

import aiofiles
from fastapi import File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from app.background_tasks.conversion import (
    change_audio_sample_rate,
    convert_video_to_audio,
)
from app.utils.file_manager import FileManager
from app.utils.responses import Accepted


class FileService(FileManager):
    arcname: str = "transcription"

    def __init__(self) -> None:
        """
        File Service
        :return -> None
        """

        super().__init__()

    async def _generate_zip(self, files: list[Path]) -> BytesIO | Exception:
        """
        Generate zip file
        :param -> files: list[Path]
        :return -> BytesIO | Exception
        """

        try:
            zip_stream = io.BytesIO()

            with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    zipf.write(file, arcname=FileService.arcname + file.suffix)

            return zip_stream

        except Exception as e:
            raise Exception(
                {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "detail": "Error: Zip file generation failed",
                }
            ) from e

    async def download(self, file_id: str) -> StreamingResponse | HTTPException:
        """
        Download file
        :param -> file_id: str
        :return -> StreamingResponse | HTTPException
        """

        try:
            files: list[Path] = self.get_transcription_files(file_id=file_id)

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: File not found",
            ) from e

        try:
            # Generate the ZIP archive asynchronously
            zip_stream: BytesIO = await self._generate_zip(files=files)

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
                convert_video_to_audio.delay(
                    data={
                        "file_id": file_id,
                        "video_path": file_path,
                        "video_extension": file_extension[1:],
                        "audio_format": "wav",
                        "delete_original_file": True,
                    }
                )

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

    async def delete(self, file_id: str) -> None | HTTPException:
        """
        Delete file
        :param -> file_id: str
        :return -> None | HTTPException
        """

        try:
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

    async def list(self) -> list[dict] | HTTPException:
        """
        List files
        :return -> list[dict] | HTTPException
        """

        try:
            pass

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: List service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

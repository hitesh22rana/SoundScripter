# Purpose: Upload service to handle file upload related tasks
# Path: backend/app/services/files/upload.py


import aiofiles
from fastapi import File, HTTPException, UploadFile, status

from app.background_tasks.conversion import (
    change_audio_sample_rate,
    convert_video_to_audio,
)
from app.utils.file_manager import FileManager
from app.utils.responses import Accepted


class UploadService(FileManager):
    def __init__(self, file: UploadFile = File(...)) -> None | HTTPException:
        """
        Upload service
        :param -> file: UploadFile
        :return -> None | HTTPException
        """

        super().__init__()

        self.file: UploadFile = file
        self.file_id: str = self.get_unique_file_id()
        self.file_extension: str = self.get_file_extension(file_name=self.file.filename)

        if (
            not self.validate_payload_file_type(self.file.content_type)
            or not self.file_extension
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Invalid file type",
            )

        self.file_path: str = self.generate_file_path(
            file_name=self.file_id, file_extension=self.file_extension
        )

    async def upload(self) -> None | HTTPException:
        """
        Upload file
        :return -> Accepted | HTTPException
        """

        try:
            async with aiofiles.open(self.file_path, "wb") as f:
                while chunk := await self.file.read(
                    self.chunk_size_bytes * self.chunk_size_bytes
                ):
                    await f.write(chunk)

            if self.is_audio_file_extension(self.file_extension[1:]):
                change_audio_sample_rate.delay(
                    data={
                        "file_id": self.file_id,
                        "audio_path": self.file_path,
                        "audio_format": self.file_extension[1:],
                        "sample_rate": 16000,  # 16 kHz
                        "output_path": self.file_path.replace(
                            self.file_extension[1:], "wav"
                        ),
                        "output_format": "wav",
                        "delete_original_file": True,
                    }
                )

            elif self.is_video_file_extension(self.file_extension[1:]):
                convert_video_to_audio.delay(
                    data={
                        "file_id": self.file_id,
                        "video_path": self.file_path,
                        "video_extension": self.file_extension[1:],
                        "audio_format": "wav",
                        "delete_original_file": True,
                    }
                )

            return Accepted(
                {
                    "file_id": self.file_id,
                    "detail": f"Success: File uploaded successfully",
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Upload service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

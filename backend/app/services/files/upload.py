# Purpose: Upload service to handle file upload related tasks
# Path: backend/app/services/files/upload.py


import aiofiles
from fastapi import BackgroundTasks, File, HTTPException, UploadFile, status

from app.services.files import FileService
from app.utils.responses import Accepted


class UploadService(FileService):
    """
    Upload service
    """

    def __init__(self, file: UploadFile = File(...)) -> None | HTTPException:
        """
        Upload service
        :param file: UploadFile
        :return None | HTTPException
        """

        super().__init__()

        self.file: UploadFile = file
        self.file_name: str = self.get_unique_file_name()
        self.file_extension: str = self.get_file_extension(file_name=self.file.filename)
        self.file_path: str = self.generate_file_path(
            file_name=self.file_name, file_extension=self.file_extension
        )

        if (
            not self.validate_file_type(self.file.content_type)
            or not self.file_extension
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Bad Request",
            )

    async def upload(self, background_tasks: BackgroundTasks) -> None | HTTPException:
        """
        Upload file
        :param file: UploadFile
        :return: Accepted | HTTPException
        """

        try:
            async with aiofiles.open(self.file_path, "wb") as f:
                while chunk := await self.file.read(
                    self.chunk_size_bytes * self.chunk_size_bytes
                ):
                    await f.write(chunk)

            if not self.is_audio_file_extension(
                self.file_extension[1:]
            ) and self.is_video_file_extension(self.file_extension[1:]):
                # Lazy import VideoToAudio
                from app.utils.video_to_audio import VideoToAudio

                self.video_to_audio: VideoToAudio = VideoToAudio(
                    video_path=self.file_path,
                    video_extension=self.file_extension,
                    audio_extension=".mp3",
                    delete_original_file=True,
                )
                background_tasks.add_task(self.video_to_audio.convert)

            return Accepted({"details": f"File {self.file_name} uploaded successfully"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

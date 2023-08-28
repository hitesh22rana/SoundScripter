# Purpose: Download service to handle file download related tasks
# Path: backend/app/services/files/download.py

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from app.services.files import FileService


class DownloadService(FileService):
    """
    Download service
    """

    def __init__(self, file_name):
        """
        Download service

        :param file_name: str
        """

        self.file_name = file_name
        self.file_path = self.get_file_path(self.file_name)

        if not self.validate_file_path(self.file_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Bad Request",
            )

    async def download(self) -> FileResponse:
        """
        Download file
        :param file: UploadFile
        :return: FileResponse
        """

        return FileResponse(
            path=self.file_path,
            filename=self.file_name,
        )

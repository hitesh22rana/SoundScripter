# Purpose: Upload service to handle file upload related tasks
# Path: backend/app/services/files/upload.py


import aiofiles
from fastapi import File, HTTPException, UploadFile, status

from app.services.files import FileService
from app.utils.responses import Accepted


class UploadService(FileService):
    """
    Upload service
    """

    def __init__(self, file: UploadFile = File(...)) -> None:
        """
        Upload service
        :param file: UploadFile
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

    async def upload(self) -> Accepted | HTTPException:
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

            return Accepted({"details": f"File {self.file_name} uploaded successfully"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

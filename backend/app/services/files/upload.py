# Purpose: Upload service to handle file upload related tasks
# Path: backend/app/services/files/upload.py

from datetime import datetime
from uuid import uuid4

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

        self.file = file
        self.file_name = self.get_unique_file_name(self.file.filename)
        self.file_path = self.get_file_path(self.file_name)

        if not self.validate_file_type(self.file.content_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Bad Request",
            )

    def get_unique_file_name(self, file_name: str) -> str:
        """
        Generate a unique file name
        :param file_name: str
        :return: str
        """
        return (
            datetime.now().strftime("%Y%m-%d%H-%M%S-")
            + str(uuid4())
            + file_name.strip().replace(" ", "_")
        )

    async def upload(self) -> Accepted | HTTPException:
        """
        Upload file
        :param file: UploadFile
        :return: Accepted | HTTPException
        """

        try:
            with open(self.file_path, "wb") as f:
                while contents := await self.file.read(self.chunk_size_bytes):
                    f.write(contents)

            return Accepted(
                content={"message": f"File {self.file_name} uploaded successfully"}
            )

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

        finally:
            self.file.file.close()

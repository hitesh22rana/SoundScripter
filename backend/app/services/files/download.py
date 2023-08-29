# Purpose: Download service to handle file download related tasks
# Path: backend/app/services/files/download.py

import io
import zipfile
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from app.services.files import FileService


class DownloadService(FileService):
    """
    Download service
    """

    def __init__(self, file_id: str):
        """
        Download service

        :param file_id: str
        """

        self.file_id = file_id
        self.file_path: Path = Path(self.get_transcription_file_path(self.file_id))

        if not self.validate_file_path(self.file_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error: Bad Request",
            )

    async def generate_zip(self) -> BytesIO:
        """
        Generate zip file
        :return: BytesIO
        """
        zip_stream = io.BytesIO()

        with zipfile.ZipFile(zip_stream, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in self.file_path.glob("**/*"):
                if file.is_file():
                    relative_path = file.relative_to(self.file_path)
                    zipf.write(file, arcname=str(relative_path))

        return zip_stream

    async def download(self) -> StreamingResponse:
        """
        Download file
        :param file: UploadFile
        :return: FileResponse
        """

        # Generate the ZIP archive asynchronously
        zip_stream: BytesIO = await self.generate_zip()

        # Serve the ZIP archive as a downloadable file
        return StreamingResponse(
            io.BytesIO(zip_stream.getvalue()),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={self.file_id}.zip"},
        )

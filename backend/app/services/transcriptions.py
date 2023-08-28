# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from fastapi import HTTPException, status

from app.schemas import TranscriptionSchema
from app.services.files import FileService
from app.utils.docker_client import docker_client
from app.utils.responses import OK


class TranscriptionService:
    def __init__(self, transcription_details: TranscriptionSchema) -> None:
        self.file_service = FileService()

        self.file_id = transcription_details.file_id
        self.language = transcription_details.language
        self.file_extension = transcription_details.file_extension

        self.file_path = self.file_service.get_file_path(
            file_id=self.file_id, file_extension=self.file_extension
        )

        if not self.file_service.validate_file_path(file_path=self.file_path):
            raise HTTPException(status_code=404, detail="File not found")

    async def transcribe(self):
        try:
            docker_client.run_transcription_service(
                file_id=self.file_id,
                file_extension=self.file_extension,
                language=self.language,
            )

            return OK({"detail": "File is added to transcription queue"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

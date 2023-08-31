# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from fastapi import HTTPException, status

from app.schemas import TranscriptionSchema
from app.services.files import FileService
from app.utils.docker_client import docker_client
from app.utils.responses import OK


class TranscriptionService:
    def __init__(
        self,
        transcription_details: TranscriptionSchema,
    ) -> None | HTTPException:
        self.file_service: FileService = FileService()

        self.file_id: str = transcription_details.file_id
        self.language: str = transcription_details.language

        try:
            self.file_path: str = self.file_service.get_file_path_from_id(
                file_id=self.file_id
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            ) from e

        self.file_extension: str = self.file_service.get_file_extension(
            file_name=self.file_path
        )

    async def transcribe(self) -> OK | HTTPException:
        try:
            docker_client.run_transcription_service(
                file_id=self.file_id,
                language=self.language,
            )

            return OK({"detail": "Success: File is added to transcription queue"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

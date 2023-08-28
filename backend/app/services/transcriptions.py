# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from app.schemas import TranscriptionSchema
from app.utils.docker_client import docker_client
from app.utils.responses import OK


class TranscriptionService:
    def __init__(self, transcription_details: TranscriptionSchema):
        self.file_name = transcription_details.file_name
        self.language = transcription_details.language

    async def transcribe(self) -> str:
        docker_client.run_transcription_service(
            file_name=self.file_name,
            language=self.language,
        )

        return OK({"detail": "Transcription completed successfully"})

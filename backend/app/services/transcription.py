# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from fastapi import BackgroundTasks, HTTPException, status

from app.schemas import TranscriptionSchema
from app.services.files import FileService
from app.utils.docker_client import docker_client
from app.utils.responses import OK
from app.utils.video_to_audio import VideoToAudio


class TranscriptionService:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        transcription_details: TranscriptionSchema,
    ) -> None | HTTPException:
        self.file_service: FileService = FileService()

        self.file_id: str = transcription_details.file_id
        self.language: str = transcription_details.language
        self.file_path: str = self.file_service.get_file_path_from_id(
            file_id=self.file_id
        )

        if not self.file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        self.file_extension: str = self.file_service.get_file_extension(
            file_name=self.file_path
        )

        if not self.file_service.is_audio_file_extension(
            self.file_extension[1:]
        ) and self.file_service.is_video_file_extension(self.file_extension[1:]):
            self.video_to_audio: VideoToAudio = VideoToAudio(
                video_path=self.file_path,
                video_extension=self.file_extension,
                audio_extension=".mp3",
            )
            background_tasks.add_task(self.video_to_audio.convert)

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

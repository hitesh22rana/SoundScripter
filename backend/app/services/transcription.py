# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

import os

from fastapi import HTTPException, status

from app.background_tasks.transcription import generate_transcriptions
from app.schemas import TranscriptionSchema
from app.services.files import FileService
from app.utils.responses import OK


class TranscriptionService:
    image: str = "transcription-service"
    container_base_path: str = "home/files"

    def __init__(
        self,
        transcription_details: TranscriptionSchema,
    ) -> None | HTTPException:
        self.file_service: FileService = FileService()

        self.file_id: str = transcription_details.file_id
        self.language: str = transcription_details.language
        self.model: str = "small.en" if self.language == "English" else "small"

        try:
            self.file_path: str = self.file_service.get_file_path_from_id(
                file_id=self.file_id
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            ) from e

    def get_container_config(self) -> dict:
        relative_volume_path: str = f"data/{self.file_id}"
        absolute_volume_path: str = os.path.abspath(relative_volume_path)

        container_config: dict = {
            "image": TranscriptionService.image,
            "volumes": {
                absolute_volume_path: {
                    "bind": f"/{TranscriptionService.container_base_path}",
                    "mode": "rw",
                }
            },
        }

        return container_config

    def get_file_path(self) -> str:
        return f"{TranscriptionService.container_base_path}/file.mp3"

    def get_output_folder_path(self) -> str:
        return f"{TranscriptionService.container_base_path}/transcriptions"

    async def transcribe(self) -> OK | HTTPException:
        try:
            data: dict = {
                "container_config": self.get_container_config(),
                "detach": True,
                "remove": True,
                "command": f"whisper {self.get_file_path()} --fp16 False --language {self.language} --model {self.model} --task transcribe --output_dir {self.get_output_folder_path()} --threads 2 --verbose False",
            }

            task = generate_transcriptions.delay(data=data)

            return OK(
                {
                    "task_id": task.id,
                    "detail": "Success: File is added to transcription queue",
                }
            )

        except Exception as e:
            print(e)
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Transcription service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")

            raise HTTPException(status_code=status_code, detail=detail) from e

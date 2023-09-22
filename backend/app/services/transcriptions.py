# Purpose: Transcription service for handling transcriptions related tasks.
# Path: backend\app\services\transcriptions.py

from fastapi import HTTPException, status

from app.background_tasks.transcription import generate_transcriptions
from app.config import settings
from app.schemas import TranscriptionSchema
from app.utils.file_manager import FileManager
from app.utils.responses import OK


class TranscriptionService:
    local_storage_base_path: str = settings.local_storage_base_path

    image: str = "transcription-service"
    container_base_path: str = "home/data"

    def __init__(
        self,
        transcription_details: TranscriptionSchema,
    ) -> None | HTTPException:
        """
        Transcription Service
        :param -> transcription_details: TranscriptionSchema
        :return -> None | HTTPException
        """

        self.file_id: str = transcription_details.file_id
        self.language: str = transcription_details.language

        # TODO:- Add support for multiple languages
        if self.language != "English":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Currently only English is supported",
            )

        self.model: str = "ggml-small.en-q5_1.bin"

        self.file_manager: FileManager = FileManager()

        try:
            self.file_path: str = self.file_manager.get_file_path_from_id(
                file_id=self.file_id
            )

        except FileNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            ) from e

    def _get_container_config(self) -> dict:
        """
        Generate docker container config
        :return -> dict
        """

        bind_volume_path: str = (
            TranscriptionService.local_storage_base_path + "/" + self.file_id
        )

        container_config: dict = {
            "image": TranscriptionService.image,
            "volumes": {
                bind_volume_path: {
                    "bind": f"/{TranscriptionService.container_base_path}",
                    "mode": "rw",
                }
            },
        }

        return container_config

    def _get_file_path(self) -> str:
        """
        Generate relative file path for the audio file
        :return -> str
        """

        return f"/{TranscriptionService.container_base_path}/file.wav"

    def _get_output_folder_path(self) -> str:
        """
        Generate relative output folder path for the audio file
        :return -> str
        """

        return f"/{TranscriptionService.container_base_path}/transcriptions"

    def _get_model_path(self) -> str:
        """
        Generate relative model path
        :return -> str
        """

        return f"/root/models/{self.model}"

    async def transcribe(self) -> OK | HTTPException:
        """
        Add the transcription request in the task queue for further processing
        :return -> OK | HTTPException
        """

        try:
            task = generate_transcriptions.delay(
                data={
                    "file_id": self.file_id,
                    "container_config": self._get_container_config(),
                    "detach": False,
                    "remove": True,
                    "command": f"whisper -t 2 -m {self._get_model_path()} -f {self._get_file_path()} -osrt -ovtt -of {self._get_output_folder_path()}",
                }
            )

            return OK(
                {
                    "task_id": task.id,
                    "detail": "Success: File is added to transcription queue",
                }
            )

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Transcription service is not available"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")

            raise HTTPException(status_code=status_code, detail=detail) from e
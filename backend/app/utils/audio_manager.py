# Purpose: AudioManager utility class for handling audio related tasks.
# Path: backend\app\utils\audio_manager.py

from fastapi import status
from pydub import AudioSegment

from app.utils.file_manager import FileManager


class AudioManager:
    def __init__(
        self,
        audio_path: str,
        audio_format: str,
    ) -> None | Exception:
        self.audio_path = audio_path
        self.audio_format = audio_format

        self.file_manager: FileManager = FileManager()

        if not self.file_manager.validate_file_path(self.audio_path):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: File not found",
                }
            )

        if not self.file_manager.is_audio_file_extension(self.audio_format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

    def split_audio(
        self, part_count: int, delete_original_file: bool = False
    ) -> None | Exception:
        try:
            audio = AudioSegment.from_file(
                self.audio_path,
                format=self.audio_format,
            )

            audio_duration = len(audio)
            part_duration = audio_duration // part_count
            original_file_name = self.audio_path.replace("." + self.audio_format, "")

            for part in range(part_count):
                start_duration = part * part_duration
                end_duration = (part + 1) * part_duration

                # Check if this is the last part and add any leftover duration
                if part == part_count - 1:
                    end_duration = audio_duration

                # export audio part
                audio[start_duration:end_duration].export(
                    f"{original_file_name}{part + 1}.{self.audio_format}",
                    format=self.audio_format,
                )

            if delete_original_file:
                try:
                    self.file_manager.delete_file(self.audio_path)
                except Exception as e:
                    raise Exception(
                        {
                            "status_code": status.HTTP_404_NOT_FOUND,
                            "detail": "Error: File not found",
                        }
                    ) from e

        except Exception as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Internal server error"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise Exception({"status_code": status_code, "detail": detail}) from e

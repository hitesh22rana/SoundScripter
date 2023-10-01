# Purpose: AudioManager utility class for handling audio related tasks.
# Path: backend\app\utils\audio_manager.py

from fastapi import status
from pydub import AudioSegment

from app.utils.file_manager import FileManager


class AudioManager:
    def __init__(
        self,
        path: str,
        format: str,
    ) -> None | Exception:
        """
        AudioManager Utility
        :param -> path: str, format: str
        :return -> None | Exception
        """

        self.path = path
        self.format = format

        self.file_manager: FileManager = FileManager()

        if not self.file_manager.validate_file_path(self.path):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: File not found",
                }
            )

        if not self.file_manager.is_audio_file_extension(self.format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

    def change_sample_rate(
        self,
        sample_rate: str,
        output_path: str,
        output_format: str,
        delete_original_file: bool = False,
    ) -> None | Exception:
        """
        Changes audio sample rate
        :param -> sample_rate: str, output_path: str, output_format: str, delete_original_file: bool
        :return -> None | Exception
        """

        if not self.file_manager.is_audio_file_extension(output_format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

        try:
            audio = AudioSegment.from_file(
                self.path,
                format=self.format,
            )

            audio.export(
                out_f=output_path,
                format=output_format,
                parameters=[
                    "-ac",
                    "1",
                    "-ar",
                    str(sample_rate),
                    "-acodec",
                    "pcm_s16le",
                ],
            )

            if delete_original_file and output_path != self.path:
                try:
                    self.file_manager.delete_file(self.path)
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

    def split_audio(
        self, part_count: int, delete_original_file: bool = False
    ) -> None | Exception:
        """
        Split audio into multiple parts
        :param -> part_count: int, delete_original_file: bool
        :return -> None | Exception
        """

        try:
            audio = AudioSegment.from_file(
                self.path,
                format=self.format,
            )

            audio_duration = len(audio)
            part_duration = audio_duration // part_count
            original_file_name = self.path.replace("." + self.format, "")

            for part in range(part_count):
                start_duration = part * part_duration
                end_duration = (part + 1) * part_duration

                # Check if this is the last part and add any leftover duration
                if part == part_count - 1:
                    end_duration = audio_duration

                # export audio part
                audio[start_duration:end_duration].export(
                    f"{original_file_name}{part + 1}.{self.format}",
                    format=self.format,
                )

            if delete_original_file:
                try:
                    self.file_manager.delete_file(self.path)
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

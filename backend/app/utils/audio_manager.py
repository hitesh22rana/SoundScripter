# Purpose: AudioManager utility class for handling audio related tasks.
# Path: backend\app\utils\audio_manager.py

from fastapi import status
from pydub import AudioSegment

from app.utils.file_manager import file_manager


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

        if not file_manager.validate_file_path(self.path):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: File not found",
                }
            )

        if not file_manager.is_audio_file_extension(self.format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

        self.audio = AudioSegment.from_file(
            file=self.path,
            format=self.format,
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

        if not file_manager.is_audio_file_extension(output_format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

        try:
            self.audio.export(
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
                    file_manager.delete_file(self.path)
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

    def get_audio_split_offset(self, parts_count: int) -> float:
        """
        Get audio split offset in seconds
        :param -> parts_count: int
        :return -> float
        """

        return round(((len(self.audio) // parts_count) / 1000), 3)

    def split_audio(
        self,
        parts_count: int,
        delete_original_file: bool = False,
    ) -> None | Exception:
        """
        Split audio into multiple parts
        :param -> parts_count: int, delete_original_file: bool
        :return -> None | Exception
        """

        try:
            duration = len(self.audio)
            part_duration = duration // parts_count
            original_file_name = self.path.replace("." + self.format, "")

            for part in range(parts_count):
                start_duration = part * part_duration
                end_duration = (part + 1) * part_duration

                # Check if this is the last part and add any leftover duration
                if part == parts_count - 1:
                    end_duration = duration

                # export audio part
                self.audio[start_duration:end_duration].export(
                    f"{original_file_name}{part + 1}.{self.format}",
                    format=self.format,
                )

            if delete_original_file:
                try:
                    file_manager.delete_file(self.path)
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

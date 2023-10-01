# Purpose: VideoManager utility class for handling video to audio conversion tasks.
# Path: backend\app\utils\video_manager.py

from fastapi import status
from moviepy.editor import AudioFileClip, VideoFileClip

from app.utils.file_manager import FileManager


class VideoManager:
    def __init__(self, path: str, format: str) -> None | Exception:
        """
        VideoManager Utility
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

    def convert_to_audio(
        self, output_path: str, output_format: str, delete_original_file: bool = False
    ) -> None | Exception:
        """
        Converts video to audio
        :param -> output_path: str, output_format: str, delete_original_file: bool
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
            video_file: VideoFileClip = VideoFileClip(self.path)
            audio_file: AudioFileClip = video_file.audio
            audio_file.write_audiofile(
                filename=output_path,
                nbytes=2,
                codec="pcm_s16le",
                buffersize=8192,
                verbose=False,
                logger=None,
            )

            video_file.close()
            audio_file.close()

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

# Purpose: VideoManager utility class for handling video to audio conversion tasks.
# Path: backend\app\utils\video_manager.py

from fastapi import status
from moviepy.editor import AudioFileClip, VideoFileClip

from app.utils.file_manager import FileManager
from app.utils.responses import OK


class VideoManager:
    def __init__(self, video_path: str, video_extension: str) -> None:
        self.video_path = video_path
        self.video_extension = video_extension

        self.file_manager: FileManager = FileManager()

        if not self.file_manager.validate_file_path(self.video_path):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: File not found",
                }
            )

    def convert_to_audio(
        self, audio_format: str, delete_original_file: bool = False
    ) -> OK | Exception:
        if not self.file_manager.is_audio_file_extension(audio_format):
            raise Exception(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "detail": "Error: Invalid audio format",
                }
            )

        audio_path = self.video_path.replace(self.video_extension, audio_format)

        try:
            video_file: VideoFileClip = VideoFileClip(self.video_path)
            audio_file: AudioFileClip = video_file.audio
            audio_file.write_audiofile(
                filename=audio_path,
                nbytes=2,
                buffersize=8192,
                codec="libmp3lame",
                verbose=False,
                logger=None,
            )

            video_file.close()
            audio_file.close()

            if delete_original_file:
                try:
                    self.file_manager.delete_file(self.video_path)
                except Exception as e:
                    raise Exception(
                        {
                            "status_code": status.HTTP_400_BAD_REQUEST,
                            "detail": "Error: Bad Request",
                        }
                    ) from e

            return OK({"detail": "Success: File converted"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise Exception({"status_code": status_code, "detail": detail}) from e

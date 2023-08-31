# Purpose: VideoToAudio utility class for handling video to audio conversion tasks.
# Path: backend\app\utils\video_to_audio.py

from fastapi import HTTPException, status
from moviepy.editor import AudioFileClip, VideoFileClip

from app.utils.responses import OK


class VideoToAudio:
    def __init__(
        self,
        video_path: str,
        video_extension: str,
        audio_extension: str = ".mp3",
        delete_original_file: bool = False,
    ) -> None:
        self.video_path = video_path
        self.audio_path = self.video_path.replace(video_extension, audio_extension)
        self.delete_original_file = delete_original_file

    def convert(self) -> OK | HTTPException:
        try:
            video_file: VideoFileClip = VideoFileClip(self.video_path)
            audio_file: AudioFileClip = video_file.audio
            audio_file.write_audiofile(
                filename=self.audio_path,
                nbytes=2,
                buffersize=8192,
                codec="libmp3lame",
                verbose=False,
                logger=None,
            )

            video_file.close()
            audio_file.close()

            if self.delete_original_file:
                # Lazy import FileService
                from app.services.files import FileService

                file_service: FileService = FileService()

                try:
                    file_service.delete_file(self.video_path)
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Error: Bad Request",
                    ) from e

            return OK({"detail": "Success: File converted"})

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            detail = "Error: Bad Request"

            if isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e

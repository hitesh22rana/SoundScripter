# Purpose: Background task for converting video to audio.
# Path: backend\app\background_tasks\conversion.py

from app.background_tasks import background_tasks
from app.utils.video_manager import VideoManager


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="conversion_task_queue",
)
def convert_video_to_audio(data: dict) -> None:
    try:
        # TODO:- Notify the user that the video is being converted
        print("Converting video to audio")

        VideoManager(
            video_path=data["video_path"], video_extension=data["video_extension"]
        ).convert_to_audio(
            audio_format=data["audio_format"],
            delete_original_file=data["delete_original_file"],
        )

        # TODO:- After successfully converting the video to audio, notify the user
        print("Success: Video converted to audio")

    except Exception as e:
        print(f"Error: {e}")

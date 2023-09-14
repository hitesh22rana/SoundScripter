# Purpose: Background task for converting video to audio.
# Path: backend\app\background_tasks\conversion.py

from app.background_tasks import background_tasks
from app.utils.audio_manager import AudioManager
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

        audio_path = data["video_path"].replace(data["video_extension"], "wav")

        change_audio_sample_rate.delay(
            data={
                "audio_path": audio_path,
                "audio_format": "wav",
                "sample_rate": "16000",
                "output_path": audio_path,
                "output_format": "wav",
                "delete_original_file": True,
            }
        )

    except Exception as e:
        print(f"Error: {e}")


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="conversion_task_queue",
)
def change_audio_sample_rate(data: dict) -> None:
    try:
        # TODO:- Notify the user that the audio's sample rate is being optimised
        print("Optimising audio smaple rate")

        AudioManager(
            audio_path=data["audio_path"], audio_format=data["audio_format"]
        ).change_sample_rate(
            sample_rate=data["sample_rate"],
            output_path=data["output_path"],
            output_format=data["output_format"],
            delete_original_file=data["delete_original_file"],
        )

        # TODO:- After successfully optimsing the audio, notify the user
        print("Success: audio sample rate optimised")

    except Exception as e:
        print(f"Error: {e}")

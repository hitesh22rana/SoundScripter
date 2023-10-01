# Purpose: Background task for converting video to audio.
# Path: backend\app\background_tasks\conversion.py

from datetime import datetime, timezone

from app.background_tasks import background_tasks
from app.models import FilesModel
from app.services.sse import Channels, NotificationsService
from app.utils.audio_manager import AudioManager
from app.utils.db_client import db_client
from app.utils.shared import Channels, Status
from app.utils.video_manager import VideoManager


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="conversion_task_queue",
)
def convert_video_to_audio(data: dict) -> None:
    try:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.PROCESSING

        session.commit()
        session.refresh(file)
        session.close()

        print(f"Converting video {data['id']} to audio")

        NotificationsService().publish(
            channel=Channels.STATUS,
            message=f"Converting video {data['id']} to audio",
        )

        VideoManager(
            path=data["current_path"], format=data["current_format"]
        ).convert_to_audio(
            output_path=data["output_path"],
            output_format=data["output_format"],
            delete_original_file=data["delete_original_file"],
        )

        print(f"Success: Video {data['id']} converted to audio")

        NotificationsService().publish(
            channel=Channels.STATUS,
            message=f"Success: Video {data['id']} converted to audio",
        )

        data["current_path"] = data["output_path"]
        data["current_format"] = data["output_format"]
        change_audio_sample_rate.delay(data=data)

    except Exception as e:
        print(f"Error: {e}")

        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="conversion_task_queue",
)
def change_audio_sample_rate(data: dict) -> None:
    try:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.PROCESSING

        session.commit()
        session.refresh(file)

        print(f"Optimising audio smaple rate for {data['id']} audio")

        NotificationsService().publish(
            channel=Channels.STATUS,
            message=f"Optimising audio smaple rate for {data['id']} audio",
        )

        AudioManager(
            path=data["current_path"], format=data["current_format"]
        ).change_sample_rate(
            sample_rate=data["sample_rate"],
            output_path=data["output_path"],
            output_format=data["output_format"],
            delete_original_file=data["delete_original_file"],
        )

        print(f"Success: {data['id']} audio sample rate optimised")

        NotificationsService().publish(
            channel=Channels.STATUS,
            message=f"Success: {data['id']} audio sample rate optimised",
        )

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.path = data["output_path"]
        file.status = Status.DONE
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()

    except Exception as e:
        print(f"Error: {e}")

        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()

# Purpose: Background task for converting video to audio.
# Path: backend\app\background_tasks\conversion.py

import json
from datetime import datetime, timezone

from app.background_tasks import background_tasks
from app.models import FilesModel
from app.services.sse.notifications import NotificationsService
from app.utils.audio_manager import AudioManager
from app.utils.db_client import db_client
from app.utils.shared import Channels, NotificationType, Status, Task
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

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.PROCESSING,
                    "type": NotificationType.INFO,
                    "task": Task.CONVERSION,
                    "message": "video to audio conversion in process",
                }
            ),
        )

        VideoManager(
            path=data["current_path"], format=data["current_format"]
        ).convert_to_audio(
            output_path=data["output_path"],
            output_format=data["output_format"],
            delete_original_file=data["delete_original_file"],
        )

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.PROCESSING,
                    "type": NotificationType.SUCCESS,
                    "task": Task.CONVERSION,
                    "message": "successfully converted video to audio",
                }
            ),
        )

        data["current_path"] = data["output_path"]
        data["current_format"] = data["output_format"]
        change_audio_sample_rate.delay(data=data)

    except Exception as _:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.ERROR,
                    "type": NotificationType.ERROR,
                    "task": Task.CONVERSION,
                    "message": "video to audio conversion failed",
                }
            ),
        )


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

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.PROCESSING,
                    "type": NotificationType.INFO,
                    "task": Task.OPTIMIZATION,
                    "message": "audio optimization in process",
                }
            ),
        )

        AudioManager(
            path=data["current_path"], format=data["current_format"]
        ).change_sample_rate(
            sample_rate=data["sample_rate"],
            output_path=data["output_path"],
            output_format=data["output_format"],
            delete_original_file=data["delete_original_file"],
        )

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.path = data["output_path"]
        file.status = Status.DONE
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.DONE,
                    "type": NotificationType.SUCCESS,
                    "task": Task.OPTIMIZATION,
                    "message": "successfully optimized audio",
                }
            ),
        )

    except Exception as _:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        file.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(file)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.ERROR,
                    "type": NotificationType.ERROR,
                    "task": Task.OPTIMIZATION,
                    "message": "audio optimization failed",
                }
            ),
        )

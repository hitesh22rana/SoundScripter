# Purpose: Background task for optimizing media files.
# Path: backend\app\background_tasks\optimizaton.py

import json
from datetime import datetime, timezone

from app.background_tasks import background_tasks
from app.models import FilesModel
from app.services.sse.notifications import NotificationsService
from app.utils.audio_manager import AudioManager
from app.utils.db_client import db_client
from app.utils.file_manager import file_manager
from app.utils.shared import Channels, NotificationType, Status, Task
from app.utils.video_manager import VideoManager


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="optimization_task_queue",
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
                    "completed_at": None,
                }
            ),
        )

        VideoManager(
            path=data["current_path"],
            format=data["current_format"],
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
                    "completed_at": None,
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
        completed_at = datetime.now(timezone.utc)
        file.completed_at = completed_at

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
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="optimization_task_queue",
)
def change_audio_sample_rate(data: dict) -> None:
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
                    "task": Task.OPTIMIZATION,
                    "message": "audio sample rate optimization in process",
                    "completed_at": None,
                }
            ),
        )

        AudioManager(
            path=data["current_path"],
            format=data["current_format"],
        ).change_sample_rate(
            sample_rate=data["sample_rate"],
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
                    "task": Task.OPTIMIZATION,
                    "message": "successfully optimized audio sample rate",
                    "completed_at": None,
                }
            ),
        )

        data["current_path"] = data["output_path"]
        data["current_format"] = data["output_format"]
        split_audio_into_parts.delay(data=data)

    except Exception as _:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        completed_at = datetime.now(timezone.utc)
        file.completed_at = completed_at

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
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="optimization_task_queue",
)
def split_audio_into_parts(data: dict) -> None:
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
                    "message": "audio split in process",
                    "completed_at": None,
                }
            ),
        )

        AudioManager(
            path=data["current_path"],
            format=data["current_format"],
        ).split_audio(
            parts_count=data["parts_count"],
            delete_original_file=False,
        )

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.path = file_manager.get_folder_path(file_id=data["id"])
        file.status = Status.DONE
        completed_at = datetime.now(timezone.utc)
        file.completed_at = completed_at

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
                    "message": "successfully split audio",
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )

    except Exception as _:
        session = next(db_client.get_db_session())

        file: FilesModel = session.query(FilesModel).filter_by(id=data["id"]).first()
        file.status = Status.ERROR
        completed_at = datetime.now(timezone.utc)
        file.completed_at = completed_at

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
                    "message": "audio split failed",
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )

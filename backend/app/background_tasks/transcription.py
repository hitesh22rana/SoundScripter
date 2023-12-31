# Purpose: Background task for generating transcriptions.
# Path: backend\app\background_tasks\transcription.py

import json
from datetime import datetime, timezone

from celery import current_task

from app.background_tasks import background_tasks
from app.models import TranscriptionsModel
from app.services.sse.notifications import NotificationsService
from app.utils.db_client import db_client
from app.utils.docker_client import docker_client
from app.utils.shared import Channels, NotificationType, Status, Task


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def generate_transcription(data: dict) -> None:
    try:
        session = next(db_client.get_db_session())

        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(file_id=data["id"]).first()
        )
        transcription.task_id = current_task.request.id
        transcription.status = Status.PROCESSING

        session.commit()
        session.refresh(transcription)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.PROCESSING,
                    "type": NotificationType.INFO,
                    "task": Task.TRANSCRIPTION,
                    "message": "transcription in process",
                    "completed_at": None,
                }
            ),
        )

        docker_client.run_container(
            container_config=data["container_config"],
            name=current_task.request.id,
            detach=data["detach"],
            remove=data["remove"],
            command=data["command"],
        )

        session = next(db_client.get_db_session())
        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(file_id=data["id"]).first()
        )
        transcription.status = Status.DONE
        completed_at = datetime.now(timezone.utc)
        transcription.completed_at = completed_at

        session.commit()
        session.refresh(transcription)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.DONE,
                    "type": NotificationType.SUCCESS,
                    "task": Task.TRANSCRIPTION,
                    "message": "successfully generated transcription",
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )

    except Exception as _:
        session = next(db_client.get_db_session())

        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(file_id=data["id"]).first()
        )

        if not transcription:
            return

        transcription.status = Status.ERROR
        completed_at = datetime.now(timezone.utc)
        transcription.completed_at = completed_at

        session.commit()
        session.refresh(transcription)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.ERROR,
                    "type": NotificationType.ERROR,
                    "task": Task.TRANSCRIPTION,
                    "message": "transcription generation failed",
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )


# TODO:- Explicit error handling and robust notification
@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def terminate_transcription(container_id: str):
    try:
        session = next(db_client.get_db_session())

        docker_client.stop_container(container_id=container_id)

        session.query(TranscriptionsModel).filter_by(task_id=container_id).delete()
        session.commit()
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": container_id,
                    "status": Status.DONE,
                    "type": NotificationType.SUCCESS,
                    "task": Task.TERMINATE,
                    "message": "successfully stopped running transcription job",
                    "completed_at": None,
                }
            ),
        )

    except Exception as _:
        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(task_id=container_id).first()
        )

        if not transcription:
            return

        transcription.status = Status.ERROR
        completed_at = datetime.now(timezone.utc)
        transcription.completed_at = completed_at

        session.commit()
        session.refresh(transcription)
        session.close()

        NotificationsService().publish(
            channel=Channels.NOTIFICATIONS,
            message=json.dumps(
                {
                    "id": container_id,
                    "status": Status.ERROR,
                    "type": NotificationType.ERROR,
                    "task": Task.TERMINATE,
                    "message": "failed to stop running transcription job",
                    "completed_at": completed_at.isoformat(),
                }
            ),
        )

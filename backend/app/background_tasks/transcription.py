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
from app.utils.shared import Channels, Status


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
            channel=Channels.STATUS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.PROCESSING,
                    "process": "transcription",
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
        transcription.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(transcription)
        session.close()

        NotificationsService().publish(
            channel=Channels.STATUS,
            message=json.dumps(
                {
                    "id": data["id"],
                    "status": Status.DONE,
                    "process": "transcription",
                }
            ),
        )

    except Exception as _:
        session = next(db_client.get_db_session())

        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(file_id=data["id"]).first()
        )
        transcription.status = Status.ERROR
        transcription.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(transcription)
        session.close()


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def stop_transcription(container_id: str):
    try:
        session = next(db_client.get_db_session())

        docker_client.stop_container(container_id=container_id)

        session.query(TranscriptionsModel).filter_by(task_id=container_id).delete()
        session.commit()
        session.close()

    except Exception as _:
        transcription: TranscriptionsModel = (
            session.query(TranscriptionsModel).filter_by(task_id=container_id).first()
        )
        transcription.status = Status.ERROR
        transcription.completed_at = datetime.now(timezone.utc)

        session.commit()
        session.refresh(transcription)
        session.close()

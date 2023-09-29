# Purpose: Background task for generating transcriptions.
# Path: backend\app\background_tasks\transcription.py


from app.background_tasks import background_tasks
from app.services.sse import Channels, NotificationsService
from app.utils.docker_client import docker_client
from app.utils.shared import Channels


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def generate_transcriptions(data: dict) -> None:
    try:
        print(f"Generating transcriptions for {data['file_id']}")

        NotificationsService().publish(
            channel=Channels.status,
            message=f"Generating transcriptions for {data['file_id']}",
        )

        docker_client.run_container(
            container_config=data["container_config"],
            detach=data["detach"],
            remove=data["remove"],
            command=data["command"],
        )

        print(f"Success: Transcription generated for {data['file_id']}")

        NotificationsService().publish(
            channel=Channels.status,
            message=f"Success: Transcription generated for {data['file_id']}",
        )

    except Exception as e:
        print(f"Error: {e}")

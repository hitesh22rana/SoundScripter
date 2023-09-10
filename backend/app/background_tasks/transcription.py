# Purpose: Background task for generating transcriptions.
# Path: backend\app\background_tasks\transcription.py


from app.utils.celery_client import celery_client
from app.utils.docker_client import docker_client

transcription = celery_client.get_client()


@transcription.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def generate_transcriptions(data: dict) -> None:
    try:
        docker_client.run_container(
            container_config=data["container_config"],
            detach=data["detach"],
            remove=data["remove"],
            command=data["command"],
        )

        # TODO:- After the transcription is done, notifiy the user.
        print("Executed successfully")

    except Exception as e:
        print(f"Error: {e}")

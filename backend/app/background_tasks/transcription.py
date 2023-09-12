# Purpose: Background task for generating transcriptions.
# Path: backend\app\background_tasks\transcription.py


from app.background_tasks import background_tasks
from app.utils.docker_client import docker_client


@background_tasks.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def generate_transcriptions(data: dict) -> None:
    try:
        print("Generating transcriptions")

        docker_client.run_container(
            container_config=data["container_config"],
            detach=data["detach"],
            remove=data["remove"],
            command=data["command"],
        )

        # TODO:- After successfully generating the transcription, notifiy the user.
        print("Success: Transcription is generated")

    except Exception as e:
        print(f"Error: {e}")

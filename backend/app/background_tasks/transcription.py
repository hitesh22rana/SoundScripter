# Purpose: Background task for generating transcriptions.
# Path: backend\app\background_tasks\transcription.py


from app.utils.celery_client import celery_client

transcription = celery_client.get_client()


@transcription.task(
    acks_late=True,
    max_retries=1,
    default_retry_delay=60,
    queue="transcription_task_queue",
)
def generate_transcriptions(data: dict) -> None:
    try:
        print("Start")
        import time

        time.sleep(10)  # Simulate work
        print("End")
    except Exception as e:
        print(f"Error: {e}")

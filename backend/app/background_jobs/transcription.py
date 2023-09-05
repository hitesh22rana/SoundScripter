from app.utils.celery_client import celery_client

transcription = celery_client.get_client()


@transcription.task(queue="transcription_task_queue")
def generate_transcriptions(data: dict) -> None:
    try:
        print("Start")
        import time

        time.sleep(10)  # Simulate work
        print("End")
    except Exception as e:
        print(f"Error: {e}")

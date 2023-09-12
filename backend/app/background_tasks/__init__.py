from app.utils.celery_client import celery_client

background_tasks = celery_client.get_client()

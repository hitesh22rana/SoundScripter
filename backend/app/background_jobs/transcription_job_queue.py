# # Purpose: Transcription job queue
# # Path: backend\app\background_jobs/transcription_job_queue.py

# from rq import Queue

# from app.utils.docker_client import docker_client
# from app.utils.redis_client import redis_client


# class TranscriptionJobQueue:
#     transcription_job_queue: Queue = None
#     job_queue_name: str = "transcription_job_queue"

#     @classmethod
#     def __init__(cls):
#         cls.transcription_job_queue = Queue(
#             name=cls.job_queue_name,
#             connection=redis_client.get_client(),
#             is_async=False,
#         )

#     @classmethod
#     def add_job(
#         cls,
#         container_config: dict,
#         detach: bool,
#         remove: bool,
#         command: str,
#     ) -> str | Exception:
#         try:
#             job_task = cls.transcription_job_queue.enqueue(
#                 docker_client.run_container,
#                 container_config=container_config,
#                 detach=detach,
#                 remove=remove,
#                 command=command,
#             )

#             return job_task.id

#         except Exception as e:
#             raise e


# transcription_job_queue = TranscriptionJobQueue()

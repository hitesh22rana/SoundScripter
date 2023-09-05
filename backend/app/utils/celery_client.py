import sys

from celery import Celery
from kombu import Exchange, Queue
from loguru import logger


class CeleryClient:
    client: Celery = None

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, level="INFO", colorize=True),
            dict(sink=sys.stderr, level="CRITICAL", colorize=True),
        ],
    )

    @classmethod
    def __init__(cls) -> None:
        cls.connect()

    @classmethod
    def connect(cls) -> None:
        try:
            if not cls.client:
                cls.client = Celery(
                    "background_tasks",
                    backend="rpc://",
                    broker="amqp://guest:guest@localhost:5672//",
                )
                cls.client.conf.worker_concurrency = 4

                # Create exchanges
                default_exchange = Exchange("default", type="direct")
                transcription_exchange = Exchange(
                    "transcription_task_queue", type="direct"
                )

                # Define queues
                cls.client.conf.task_queues = [
                    Queue("default", exchange=default_exchange, routing_key="default"),
                    Queue(
                        "transcription_task_queue",
                        exchange=transcription_exchange,
                        routing_key="transcription_task_queue",
                    ),
                ]

                cls.client.conf.task_routes = {
                    "app.background_jobs.transcription.generate_transcriptions": {
                        "queue": "transcription_task_queue",
                    },
                }

                logger.info("Success: Celery client connected")

        except Exception as _:
            logger.critical("Error: Celery client could not be connected")
            raise Exception()

    @classmethod
    def disconnect(cls) -> None:
        try:
            if cls.client:
                cls.client.close()
                logger.info("Success: Celery client disconnected")

        except Exception as _:
            logger.critical("Error: Celery client could not be disconnected")
            raise Exception()

    @classmethod
    def get_client(cls) -> Celery:
        if not cls.client:
            cls.connect()

        return cls.client


celery_client = CeleryClient()

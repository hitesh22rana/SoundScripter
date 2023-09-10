# Purpose: Celery client for handling celery tasks.
# Path: backend\app\utils\celery_client.py

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
                    broker="pyamqp://guest:guest@localhost:5672//",
                    include=["app.background_tasks.transcription"],
                )
                cls.client.conf.worker_concurrency = 4

                # Queues and Exchanges
                cls.client.conf.task_queues = [
                    Queue(
                        "default",
                        exchange=Exchange("default", type="direct"),
                        routing_key="default",
                    ),
                    Queue(
                        "transcription_task_queue",
                        exchange=Exchange("transcription_task_queue", type="direct"),
                        routing_key="transcription_task_queue",
                    ),
                ]

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

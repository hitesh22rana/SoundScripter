# Purpose: Celery client for handling celery tasks.
# Path: backend\app\utils\celery_client.py

import sys

from celery import Celery
from kombu import Exchange, Queue
from loguru import logger

from app.config import settings


class CeleryClient:
    client: Celery = None

    backend: str = settings.celery_backend
    broker: str = settings.celery_broker
    worker_concurrency: str = settings.worker_concurrency

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, level="INFO", colorize=True),
            dict(sink=sys.stderr, level="CRITICAL", colorize=True),
        ],
    )

    @classmethod
    def __init__(cls) -> None | Exception:
        cls.connect()

    @classmethod
    def connect(cls) -> None | Exception:
        try:
            if not cls.client:
                cls.client = Celery(
                    "background_tasks",
                    backend=cls.backend,
                    broker=cls.broker,
                    include=[
                        "app.background_tasks.conversion",
                        "app.background_tasks.transcription",
                    ],
                )

                # Worker Concurrency
                cls.client.conf.worker_concurrency = cls.worker_concurrency

                # Queues and Exchanges
                cls.client.conf.task_queues = [
                    Queue(
                        "default",
                        exchange=Exchange("default", type="direct"),
                        routing_key="default",
                    ),
                    Queue(
                        "conversion_task_queue",
                        exchange=Exchange("conversion_task_queue", type="direct"),
                        routing_key="conversion_task_queue",
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
    def disconnect(cls) -> None | Exception:
        try:
            if cls.client:
                cls.client.close()
                logger.info("Success: Celery client disconnected")

        except Exception as _:
            logger.critical("Error: Celery client could not be disconnected")
            raise Exception()

    @classmethod
    def get_client(cls) -> Celery | None:
        if not cls.client:
            cls.connect()

        return cls.client


celery_client = CeleryClient()

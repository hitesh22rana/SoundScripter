# Purpose: Docker client for handling docker operations
# Path: backend\app\utils\docker_client.py

import sys

import docker
from fastapi import status
from loguru import logger

from app.config import settings


class DockerClient:
    client = None
    max_concurrent_containers: int = settings.max_concurrent_containers

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
                cls.client = docker.from_env()
                logger.info("Success: Docker client connected")

        except docker.errors.DockerException:
            logger.critical("Error: Docker client could not be connected")
            raise Exception()

    @classmethod
    def disconnect(cls) -> None:
        try:
            if cls.client:
                cls.client.close()
                logger.info("Success: Docker client disconnected")

        except docker.errors.DockerException:
            logger.critical("Error: Docker client could not be disconnected")
            raise Exception()

    @classmethod
    def get_client(cls) -> docker.DockerClient | None:
        if not cls.client:
            cls.connect()

        return cls.client

    @classmethod
    def run_container(
        cls,
        container_config: dict,
        detach: bool,
        remove: bool,
        command: str,
    ) -> None | Exception:
        try:
            return cls.client.containers.run(
                **container_config,
                detach=detach,
                remove=remove,
                command=command,
            )

        except Exception as e:
            logger.critical("Error: Docker client service unavailable")
            raise Exception(
                {
                    "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
                    "detail": "Error: Docker client service unavailable",
                }
            ) from e


docker_client = DockerClient()

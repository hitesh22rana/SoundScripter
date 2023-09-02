# Purpose: Docker client for handling docker operations
# Path: backend\app\utils\docker_client.py

import sys

import docker
from loguru import logger


class DockerClient:
    client = None

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, level="INFO", colorize=True),
            dict(sink=sys.stderr, level="CRITICAL", colorize=True),
        ],
    )

    @classmethod
    def __init__(cls) -> None:
        try:
            if not cls.client:
                cls.client = docker.from_env()
                logger.info("Docker client initialized")

        except docker.errors.DockerException:
            logger.error("Docker client could not be initialized")


docker_client = DockerClient()

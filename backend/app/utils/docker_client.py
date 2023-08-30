# Purpose: Docker client for handling docker operations
# Path: backend\app\utils\docker_client.py

import os
import sys

import docker
from fastapi import status
from loguru import logger


class DockerClient:
    client = None

    image: str = "transcription-service"
    container_base_path: str = "home/files"

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

    @classmethod
    def get_file_path(cls) -> str:
        return f"{cls.container_base_path}/file.mp3"

    @classmethod
    def get_output_folder_path(cls) -> str:
        return f"{cls.container_base_path}/transcriptions"

    @classmethod
    def get_container_config(cls, file_id: str):
        relative_volume_path: str = f"data/{file_id}"
        absolute_volume_path: str = os.path.abspath(relative_volume_path)

        container_config: dict = {
            "image": cls.image,
            "volumes": {
                absolute_volume_path: {
                    "bind": f"/{cls.container_base_path}",
                    "mode": "rw",
                }
            },
        }

        return container_config

    @classmethod
    def run_transcription_service(cls, file_id: str, language: str) -> None | Exception:
        # TODO: Provide the model name as a parameter based on language to boost the performance
        container_config: dict = cls.get_container_config(file_id=file_id)

        try:
            return cls.client.containers.run(
                **container_config,
                detach=True,
                remove=True,
                command=f"whisper {cls.get_file_path()} --fp16 False --language {language} --task transcribe --output_dir {cls.get_output_folder_path()} --threads 2 --verbose False",
            )

        except docker.errors.ContainerError as e:
            logger.error("Docker container could not be initialized")
            raise Exception(
                {
                    "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
                    "detail": "Transcription service is not available",
                }
            ) from e

        except docker.errors.ImageNotFound as e:
            logger.error("Docker image could not be found")
            raise Exception(
                {
                    "status_code": status.HTTP_503_SERVICE_UNAVAILABLE,
                    "detail": "Transcription service is not available",
                }
            ) from e


docker_client = DockerClient()

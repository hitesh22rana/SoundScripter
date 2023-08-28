# Purpose: Docker client for handling docker operations
# Path: backend\app\utils\docker_client.py

import os

import docker


class DockerClient:
    client = None

    image: str = "transcription-service"
    container_base_path: str = "home/files"

    relative_volume_path: str = "data"
    absolute_volume_path: str = os.path.abspath(relative_volume_path)

    container_config: dict = {
        "image": "transcription-service",
        "volumes": {
            absolute_volume_path: {"bind": f"/{container_base_path}", "mode": "rw"}
        },
    }

    @classmethod
    def __init__(cls) -> None:
        if not cls.client:
            print("Initializing docker client")
            cls.client = docker.from_env()

    @classmethod
    def run_transcription_service(cls, file_name: str, language: str):
        return cls.client.containers.run(
            **DockerClient.container_config,
            detach=True,
            remove=True,
            command=f"whisper {cls.container_base_path}/{file_name} --language {language} -o {cls.container_base_path}",
        )


docker_client = DockerClient()

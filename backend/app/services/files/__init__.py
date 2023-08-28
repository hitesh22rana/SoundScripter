# Purpose: Base Class for file services
# Path: backend/app/services/files/__init__.py

import os
from datetime import datetime
from uuid import uuid4


class FileService:
    chunk_size_bytes: int = 1024
    directory: str = "data"
    filename: str = "file"
    transcripted_files: str = "transcriptions"
    output_directory: str = "zips"
    valid_file_types: list[str] = [
        # Audio file types
        "audio/aac",
        "audio/midi",
        "audio/mpeg",
        "audio/mp4",
        "audio/ogg",
        "audio/x-flac",
        "audio/x-wav",
        "audio/amr",
        "audio/x-aiff",
        # Video file types
        "video/3gpp",
        "video/mp4",
        "video/x-m4v",
        "video/x-matroska",
        "video/webm",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-ms-wmv",
        "video/mpeg",
        "video/x-flv",
    ]

    @classmethod
    def __init__(cls) -> None:
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

        if not os.path.exists(cls.output_directory):
            os.makedirs(cls.output_directory)

    @classmethod
    def validate_file_type(cls, file_type: str) -> bool:
        """
        Validate file type
        :param file_type: str
        :return: bool
        """
        return file_type in cls.valid_file_types

    @classmethod
    def get_unique_file_name(self) -> str:
        """
        Generate a unique file name
        :param file_name: str
        :return: str
        """
        return datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid4())

    @classmethod
    def get_file_extension(cls, file_name: str) -> str:
        """
        Get file extension
        :param file_name: str
        :return: str
        """
        indx: int = file_name.rfind(".")
        return file_name[indx:] if indx != -1 else ""

    @classmethod
    def generate_file_path(cls, file_name: str, file_extension: str) -> str:
        """
        Generate file path
        :param file_name: str
        :param file_extension: str
        :return: str
        """

        os.makedirs(cls.directory + "/" + file_name, exist_ok=True)
        return cls.directory + "/" + file_name + "/" + cls.filename + file_extension

    @classmethod
    def get_transcription_file_path(cls, file_id: str) -> str:
        """
        Get file path
        :param file_name: str
        :return: str
        """
        return cls.directory + "/" + file_id + "/" + cls.transcripted_files

    @classmethod
    def get_file_path(cls, file_id: str, file_extension: str) -> str:
        """
        Get file path
        :param file_name: str
        return: str
        """
        return cls.directory + "/" + file_id + "/" + cls.filename + file_extension

    @classmethod
    def validate_file_path(cls, file_path) -> bool:
        """
        Validate file path
        :param file_path: str
        :return: bool
        """
        return os.path.exists(file_path)

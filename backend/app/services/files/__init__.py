# Purpose: Base Class for file services
# Path: backend/app/services/files/__init__.py

import os


class FileService:
    chunk_size_bytes: int = 1024 * 1024
    directory: str = "data"
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

    @classmethod
    def validate_file_type(cls, file_type: str) -> bool:
        """
        Validate file type
        :param file_type: str
        :return: bool
        """
        return file_type in cls.valid_file_types

    @classmethod
    def get_file_path(cls, file_name: str) -> str:
        """
        Get file path
        :param file_name: str
        :return: str
        """
        return cls.directory + "/" + file_name

    @classmethod
    def validate_file_path(cls, file_path) -> bool:
        """
        Validate file path
        :param file_path: str
        :return: bool
        """
        return os.path.exists(file_path)

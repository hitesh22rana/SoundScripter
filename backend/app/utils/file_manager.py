# Purpose: FileManager utility class for handling files related tasks.
# Path: backend/app/utils/file_manager.py

import os
import shutil
from datetime import datetime
from pathlib import Path
from uuid import uuid4


class FileManager:
    directory: str = "data"
    filename: str = "file"
    transcripted_files: str = "transcriptions"

    # file extensions
    audio_file_extensions: list[str] = [
        "aac",
        "mid",
        "mp3",
        "m4a",
        "wav",
        "ogg",
        "flac",
        "amr",
        "aiff",
        "mpeg",
    ]
    video_file_extensions: list[str] = [
        "3gp",
        "mp4",
        "m4v",
        "mkv",
        "webm",
        "mov",
        "avi",
        "wmv",
        "mpg",
        "flv",
    ]
    transcriptions_file_extensions: list[str] = [
        "txt",
        "srt",
        "vtt",
        "rtf",
        "json",
        "csv",
    ]

    # file mime types
    audio_file_types: list[str] = [
        "audio/aac",
        "audio/midi",
        "audio/mpeg",
        "audio/mp4",
        "audio/wav",
        "audio/ogg",
        "audio/x-flac",
        "audio/x-wav",
        "audio/amr",
        "audio/x-aiff",
    ]
    video_file_types: list[str] = [
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
        "application/octet-stream",
    ]
    transcription_file_types: list[str] = [
        "text/plain",
        "application/x-subrip",
        "text/vtt",
        "application/rtf",
        "application/json",
        "text/csv",
    ]

    @classmethod
    def __init__(cls) -> None:
        cls.make_directory(directory=cls.directory)

    @classmethod
    def make_directory(cls, directory: str) -> None:
        """
        Make directory if not already exists
        :param -> directory: str
        :return -> None
        """

        if not os.path.exists(directory):
            os.makedirs(directory)

    @classmethod
    def is_audio_file_extension(cls, file_extension: str) -> bool:
        """
        validate audio file extension
        :param -> file_extension: str
        :return -> bool
        """

        return file_extension in cls.audio_file_extensions

    @classmethod
    def is_video_file_extension(cls, file_extension: str) -> bool:
        """
        validate video file extension
        :param -> file_extension: str
        :return -> bool
        """

        return file_extension in cls.video_file_extensions

    @classmethod
    def is_transcription_file_extension(cls, file_extension: str) -> bool:
        """
        validate transcription file extension
        :param -> file_extension: str
        :return -> bool
        """

        return file_extension in cls.transcriptions_file_extensions

    @classmethod
    def is_valid_file_extension(cls, file_extension: str) -> bool:
        """
        validate payload file extension
        :param -> file_extension: str
        :return -> bool
        """

        return cls.is_audio_file_extension(
            file_extension=file_extension
        ) or cls.is_video_file_extension(file_extension=file_extension)

    @classmethod
    def is_audio_file(cls, file_type: str) -> bool:
        """
        validate audio file type
        :param -> file_type: str
        :return -> bool
        """

        return file_type in cls.audio_file_types

    @classmethod
    def is_video_file(cls, file_type: str) -> bool:
        """
        validate video file type
        :param -> file_type: str
        :return -> bool
        """

        return file_type in cls.video_file_types

    @classmethod
    def validate_payload_file_type(cls, file_type: str) -> bool:
        """
        Validate payload file type
        :param -> file_type: str
        :return -> bool
        """

        return cls.is_audio_file(file_type=file_type) or cls.is_video_file(
            file_type=file_type
        )

    @classmethod
    def validate_transcription_file_type(cls, file_type: str) -> bool:
        """
        Validate transcription file type
        :param -> file_type: str
        :return -> bool
        """

        return file_type in cls.transcription_file_types

    @classmethod
    def get_unique_file_id(self) -> str:
        """
        Generate a unique file name
        :return -> str
        """

        return datetime.now().strftime("%Y%m-%d%H-%M%S-") + str(uuid4())

    @classmethod
    def get_file_extension(cls, file_name: str) -> str:
        """
        Get file extension
        :param -> file_name: str
        :return -> str
        """

        indx: int = file_name.rfind(".")
        return file_name[indx:] if indx != -1 else ""

    @classmethod
    def generate_file_path(cls, file_name: str, file_extension: str) -> str:
        """
        Generate file path
        :param -> file_name: str, file_extension: str
        :return -> str
        """

        os.makedirs(cls.directory + "/" + file_name, exist_ok=True)
        return cls.directory + "/" + file_name + "/" + cls.filename + file_extension

    @classmethod
    def get_transcription_input_files(
        cls, file_id: str
    ) -> list[str] | FileNotFoundError:
        """
        Get transcription input files path
        :param -> file_id: str
        :return -> list[Path] | FileNotFoundError
        """

        folder: Path = Path(cls.directory + "/" + file_id)

        if not cls.validate_file_path(file_path=folder):
            raise FileNotFoundError

        files: list[str] = []
        for file in folder.glob("**/*"):
            if file.is_file() and cls.is_audio_file_extension(
                file_extension=file.suffix[1:]
            ):
                files.append(file.stem)

        if len(files) == 0:
            raise FileNotFoundError

        return files

    @classmethod
    def get_transcripted_files(cls, file_id: str) -> list[Path] | FileNotFoundError:
        """
        Get transcription files path
        :param -> file_id: str
        :return -> list[Path] | FileNotFoundError
        """

        folder: Path = Path(cls.directory + "/" + file_id)

        if not cls.validate_file_path(file_path=folder):
            raise FileNotFoundError

        files: list[Path] = []
        for file in folder.iterdir():
            if file.is_file() and cls.is_transcription_file_extension(
                file_extension=file.suffix[1:]
            ):
                files.append(Path(file))

        if len(files) == 0:
            raise FileNotFoundError

        return files

    @classmethod
    def get_generated_transcriptions(
        cls, folder: str
    ) -> list[Path] | FileNotFoundError:
        """
        Get generated transcriptions
        :param -> folder: Path
        :return -> list[Path] | FileNotFoundError
        """

        if not cls.validate_file_path(file_path=folder):
            raise FileNotFoundError

        files: list[Path] = []
        for file in Path(folder).iterdir():
            if file.is_file() and cls.is_transcription_file_extension(
                file_extension=file.suffix[1:]
            ):
                files.append(Path(file))

        if len(files) == 0:
            raise FileNotFoundError

        return files

    @classmethod
    def get_file_path(cls, file_id: str, file_extension: str) -> str:
        """
        Get file path
        :param -> file_name: str, file_extension: str
        :return -> str
        """

        return cls.directory + "/" + file_id + "/" + cls.filename + file_extension

    @classmethod
    def validate_file_path(cls, file_path) -> bool:
        """
        Validate file path
        :param -> file_path: str
        :return -> bool
        """

        return os.path.exists(file_path)

    @classmethod
    def get_folder_path(cls, file_id: str) -> str:
        """
        Get folder path
        :param -> file_id: str
        :return -> str
        """

        return cls.directory + "/" + file_id

    @classmethod
    def delete_file(cls, file_path) -> None | FileNotFoundError:
        """
        Delete file
        :param -> file_path: str
        :return -> bool | FileNotFoundError
        """

        if not cls.validate_file_path(file_path):
            raise FileNotFoundError

        return os.remove(file_path)

    @classmethod
    def delete_folder(cls, folder_path) -> None | FileNotFoundError:
        """
        Delete folder
        :param -> folder_path: str
        :return -> bool | FileNotFoundError
        """

        if not cls.validate_file_path(file_path=folder_path):
            raise FileNotFoundError

        return shutil.rmtree(folder_path)


file_manager = FileManager()

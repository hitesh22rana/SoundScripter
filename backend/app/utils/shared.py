# Purpose: Shared models and enums.
# Path: backend\app\utils\shared.py

from enum import Enum, unique

from sqlalchemy.orm import DeclarativeBase


@unique
class Channels(str, Enum):
    NOTIFICATIONS = "NOTIFICATIONS"


@unique
class Status(str, Enum):
    QUEUE = "QUEUE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"


@unique
class NotificationType(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@unique
class Task(str, Enum):
    CONVERSION = "CONVERSION"
    OPTIMIZATION = "OPTIMIZATION"
    TRANSCRIPTION = "TRANSCRIPTION"
    TERMINATE = "TERMINATE"


@unique
class Type(str, Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


@unique
class Language(str, Enum):
    ENGLISH = "en"


@unique
class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@unique
class Sort(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Base(DeclarativeBase):
    pass

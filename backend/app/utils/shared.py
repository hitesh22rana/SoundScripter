# Purpose: Shared models and enums.
# Path: backend\app\utils\shared.py

from enum import Enum, unique

from sqlalchemy.orm import DeclarativeBase


@unique
class Channels(str, Enum):
    STATUS = "STATUS"


@unique
class Status(str, Enum):
    QUEUE = "QUEUE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    ERROR = "ERROR"


@unique
class Type(str, Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


@unique
class Language(str, Enum):
    ENGLISH = "en"


@unique
class Sort(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Base(DeclarativeBase):
    pass

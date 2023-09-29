# Purpose: Shared models and enums.
# Path: backend\app\utils\shared.py

from enum import Enum, unique

from sqlalchemy.orm import DeclarativeBase


@unique
class Channels(str, Enum):
    status = "status"


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


class Base(DeclarativeBase):
    pass

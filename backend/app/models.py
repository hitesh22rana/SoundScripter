# Purpose: Database models
# Path: backend\app\models.py

import uuid
from typing import List

from sqlalchemy import ARRAY, TIMESTAMP, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ENUM as EnumPG
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.shared import Base, Language, Priority, Status, Type


class FilesModel(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=None,
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, default=None, nullable=False)
    type: Mapped[Type] = mapped_column(EnumPG(Type), default=Type.AUDIO, nullable=False)
    path: Mapped[str] = mapped_column(String, default=None, nullable=False)
    status: Mapped[Status] = mapped_column(
        EnumPG(Status), default=Status.QUEUE, nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    completed_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True
    )

    # Establish a relationship with TranscriptionsModel
    transcription: Mapped["TranscriptionsModel"] = relationship(
        "TranscriptionsModel", back_populates="file", cascade="all, delete-orphan"
    )


class TranscriptionsModel(Base):
    __tablename__ = "transcriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        nullable=False,
    )
    language: Mapped[Language] = mapped_column(
        EnumPG(Language), default=Language.ENGLISH, nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        EnumPG(Priority), default=Priority.LOW, nullable=False
    )
    status: Mapped[Status] = mapped_column(
        EnumPG(Status), default=Status.QUEUE, index=True, nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    completed_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), default=None, nullable=True
    )

    # Task ids of the celery tasks
    task_ids: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    # Foreign key to the file model and Index it for faster queries
    file_id: Mapped[str] = mapped_column(
        String, ForeignKey("files.id"), nullable=False, index=True
    )

    # Establish a relationship with FilesModel
    file: Mapped["FilesModel"] = relationship(
        "FilesModel",
        back_populates="transcription",
    )

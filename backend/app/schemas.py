# Purpose: Data and Response Schemas
# Path: backend\app\schemas.py

from typing import Optional

from pydantic import BaseModel, Field

from app.models import FilesModel, TranscriptionsModel
from app.utils.shared import Language, Priority, Status, Type


class TranscriptionSchema(BaseModel):
    file_id: str = Field(..., description="Name of the file to be transcribed")
    language: Language = Field(
        Language.ENGLISH, description="Language of the file to be transcribed"
    )
    priority: Priority = Field(
        Priority.LOW, description="Priority of the transcription job"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "XXXX-XXXX",
                "language": "en",
                "priority": "LOW",
            }
        }


class ConversionBackgroundJobPayloadSchema(BaseModel):
    id: str
    current_path: str
    current_format: str
    sample_rate: int
    output_path: str
    output_format: str
    delete_original_file: bool
    parts_count: int

    class Config:
        allow_population_by_field_name: True
        from_attributes = True


class TranscriptionBackgroundJobPayloadSchema(BaseModel):
    id: str
    container_config: dict
    detach: bool
    remove: bool
    commands: list[str]

    class Config:
        allow_population_by_field_name: True
        from_attributes = True


class FileResponse:
    def __init__(self, data: FilesModel) -> None:
        self.id: str = data.id
        self.name: str = data.name
        self.type: Type = data.type
        self.status: Status = data.status
        self.created_at: str = data.created_at.isoformat()
        self.completed_at: Optional[str] = (
            data.completed_at.isoformat() if data.completed_at else None
        )

    def response(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class TranscriptionResponse:
    def __init__(self, data: TranscriptionsModel) -> None:
        self.id: str = str(data.id)
        self.task_ids: Optional[list[str]] = data.task_ids
        self.language: str = data.language
        self.priority: Priority = data.priority
        self.status: Status = data.status
        self.created_at: str = data.created_at.isoformat()
        self.completed_at: Optional[str] = (
            data.completed_at.isoformat() if data.completed_at else None
        )

    def response(self) -> dict:
        return {
            "id": self.id,
            "task_ids": self.task_ids,
            "language": self.language,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class DataResponse:
    def __init__(self, data: list) -> None:
        self.file: FileResponse.response = FileResponse(data[0]).response()
        self.transcription: TranscriptionResponse.response = TranscriptionResponse(
            data[1]
        ).response()

    def response(self) -> dict:
        return {
            "id": self.file["id"],
            "name": self.file["name"],
            "type": self.file["type"],
            "task_ids": self.transcription["task_ids"],
            "language": self.transcription["language"],
            "priority": self.transcription["priority"],
            "status": self.transcription["status"],
            "created_at": self.transcription["created_at"],
            "completed_at": self.transcription["completed_at"],
        }

# Purpose: Models and Data Schemas
# Path: backend\app\schemas.py

from pydantic import BaseModel, Field, validator

from app.utils.shared import Status, Type
from app.utils.validators import validate_language


class TranscriptionSchema(BaseModel):
    file_id: str = Field(..., description="Name of the file to be transcribed")
    language: str = Field(..., description="Language of the file to be transcribed")

    @validator("language", pre=True)
    def validate_language(cls, language):
        return validate_language(language)

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "XXXX-XXXX",
                "language": "English",
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

    class Config:
        allow_population_by_field_name: True
        from_attributes = True


class TranscriptionBackgroundJobPayloadSchema(BaseModel):
    id: str
    container_config: dict
    detach: bool
    remove: bool
    command: str

    class Config:
        allow_population_by_field_name: True
        from_attributes = True


class DataResponse:
    def __init__(self, data) -> None:
        self.file: FileResponse.response = data[0]
        self.transcription: TranscriptionResponse.response = data[1]

    def response(self) -> dict:
        return {
            "file": FileResponse(self.file).response(),
            "transcription": TranscriptionResponse(self.transcription).response(),
        }


class FileResponse:
    def __init__(self, data) -> None:
        self.id: str = data.id
        self.type: Type = data.type
        self.status: Status = data.status
        self.created_at: str = data.created_at.isoformat()
        self.completed_at: str = (
            data.completed_at.isoformat() if data.completed_at else None
        )

    def response(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class TranscriptionResponse:
    def __init__(self, data) -> None:
        self.task_id: str = data.task_id
        self.language: str = data.language
        self.status: Status = data.status
        self.created_at: str = data.created_at.isoformat()
        self.completed_at: str = (
            data.completed_at.isoformat() if data.completed_at else None
        )

    def response(self) -> dict:
        return {
            "id": self.task_id,
            "language": self.language,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

# Purpose: Transcriptions schema
# Path: backend\app\schemas\transcriptions.py

from pydantic import BaseModel, Field, validator

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

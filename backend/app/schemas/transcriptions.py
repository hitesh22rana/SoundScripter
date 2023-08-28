# Purpose: Transcriptions schema
# Path: backend\app\schemas\transcriptions.py

from pydantic import BaseModel, Field


class TranscriptionSchema(BaseModel):
    file_id: str = Field(..., description="Name of the file to be transcribed")
    file_extension: str = Field(..., description="Type of the file to be transcribed")
    language: str = Field(..., description="Language of the file to be transcribed")

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "XXXX-XXXX",
                "file_extension": ".mp3",
                "language": "English",
            }
        }

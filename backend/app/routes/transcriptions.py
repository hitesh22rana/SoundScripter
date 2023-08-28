# Purpose: Transcription router for handling transcriptions related operations.
# Path: backend\app\routers\transcriptions.py

from fastapi import APIRouter, Body

from app.schemas import TranscriptionSchema
from app.services import TranscriptionService

router = APIRouter(
    tags=["Transcriptions"],
    prefix="/transcriptions",
)


@router.post("", response_description="Transcribe file")
async def transcribe(transcription_details: TranscriptionSchema = Body(...)):
    return await TranscriptionService(transcription_details).transcribe()

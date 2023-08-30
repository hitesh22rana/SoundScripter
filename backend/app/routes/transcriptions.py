# Purpose: Transcription router for handling transcriptions related operations.
# Path: backend\app\routers\transcriptions.py

from fastapi import APIRouter, BackgroundTasks, Body

from app.schemas import TranscriptionSchema
from app.services import TranscriptionService

router = APIRouter(
    tags=["Transcriptions"],
    prefix="/transcriptions",
)


@router.post("", response_description="Transcribe file")
async def transcribe(
    background_tasks: BackgroundTasks,
    transcription_details: TranscriptionSchema = Body(...),
):
    return await TranscriptionService(
        background_tasks=background_tasks, transcription_details=transcription_details
    ).transcribe()

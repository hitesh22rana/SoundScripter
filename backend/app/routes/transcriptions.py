# Purpose: Transcription router for handling transcriptions related operations.
# Path: backend\app\routers\transcriptions.py

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.schemas import TranscriptionSchema
from app.services.transcriptions import TranscriptionService
from app.utils.db_client import db_client
from app.utils.shared import Sort

router = APIRouter(
    tags=["Transcriptions"],
    prefix="/transcriptions",
)


@router.get("", response_description="List transcriptions")
async def list(
    session: Session = Depends(db_client.get_db_session),
    limit: int = 10,
    offset: int = 0,
    sort: Sort = Sort.DESC,
):
    return await TranscriptionService(session=session).list(
        limit=limit, offset=offset, sort=sort
    )


@router.post("", response_description="Transcribe file")
async def transcribe(
    session: Session = Depends(db_client.get_db_session),
    transcription_details: TranscriptionSchema = Body(...),
):
    return await TranscriptionService(session=session).transcribe(
        transcription_details=transcription_details
    )


@router.get("/{file_id}/download", response_description="Download transcription")
async def download(file_id: str, session: Session = Depends(db_client.get_db_session)):
    return await TranscriptionService(session=session).download(file_id=file_id)


@router.delete(
    "/{file_id}/terminate", response_description="Terminate transcription task"
)
async def terminate(file_id: str, session: Session = Depends(db_client.get_db_session)):
    return await TranscriptionService(session=session).terminate(file_id=file_id)

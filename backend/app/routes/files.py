# Purpose: Files router for handling files related operations.
# Path: backend\app\routers\files.py

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.services.files import FileService
from app.utils.db_client import db_client
from app.utils.shared import Sort

router = APIRouter(
    tags=["Files"],
    prefix="/files",
)


@router.get("", response_description="List files")
async def list(
    session: Session = Depends(db_client.get_db_session),
    limit: int = 10,
    offset: int = 0,
    sort: Sort = Sort.DESC,
):
    return await FileService(session=session).list(
        limit=limit, offset=offset, sort=sort
    )


@router.post("", response_description="Upload file")
async def upload(
    session: Session = Depends(db_client.get_db_session),
    file: UploadFile = File(...),
    name: str = Form(...),
):
    return await FileService(session=session).upload(name=name, file=file)


@router.delete("/{file_id}", response_description="Delete file")
async def delete(file_id: str, session: Session = Depends(db_client.get_db_session)):
    return await FileService(session=session).delete(file_id=file_id)

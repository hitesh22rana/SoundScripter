# Purpose: Files router for handling files related operations.
# Path: backend\app\routers\files.py

from fastapi import APIRouter, BackgroundTasks, File, UploadFile

from app.services import DownloadService, UploadService

router = APIRouter(
    tags=["Files"],
    prefix="/files",
)


@router.post("/upload", response_description="Upload file")
async def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    return await UploadService(file=file).upload(background_tasks=background_tasks)


@router.get("/download/{file_id}", response_description="Download file")
async def download(file_id: str):
    return await DownloadService(file_id=file_id).download()

# Purpose: Files router for handling files related operations.
# Path: backend\app\routers\files.py

from fastapi import APIRouter, File, UploadFile

from app.services.files import DownloadService, UploadService

router = APIRouter(
    tags=["Files"],
    prefix="/files",
)


@router.post("/upload", response_description="Upload file")
async def upload(file: UploadFile = File(...)):
    return await UploadService(file=file).upload()


@router.get("/download/{file_id}", response_description="Download file")
async def download(file_id: str):
    return await DownloadService(file_id=file_id).download()

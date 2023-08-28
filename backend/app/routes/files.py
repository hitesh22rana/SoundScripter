# Purpose: Files router for handling files related operations.
# Path: backend\app\routers\files.py

from fastapi import APIRouter, File, UploadFile

from app.services import DownloadService, UploadService

router = APIRouter(
    tags=["Files"],
    prefix="/files",
)


@router.post("/upload", response_description="Upload file")
async def upload(file: UploadFile = File(...)):
    return await UploadService(file=file).upload()


@router.get("/download/{file_name}", response_description="Download file")
async def download(file_name: str):
    return await DownloadService(file_name=file_name).download()

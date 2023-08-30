# Purpose: Main file and entry point of the application
# Path: backend\app\main.py

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import files, transcriptions

app = FastAPI(
    title="Transcription service",
    version="1.0.0",
    description="Transcription service backend",
)

"""Middleware"""
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

"""Routers"""
app.include_router(files.router)
app.include_router(transcriptions.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={
            "status_code": "422",
            "detail": f"Error: Unprocessable Entity",
        },
        status_code=422,
    )

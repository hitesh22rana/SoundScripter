# Purpose: Main file and entry point of the application
# Path: backend\app\main.py

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import files, sse, transcriptions
from app.utils.celery_client import celery_client
from app.utils.db_client import db_client
from app.utils.docker_client import docker_client
from app.utils.redis_client import redis_client

app = FastAPI(
    title="Transcription service",
    description="Transcription service backend",
    version="1.0.0",
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
app.include_router(files.router, prefix="/api/v1")
app.include_router(transcriptions.router, prefix="/api/v1")
app.include_router(sse.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    try:
        db_client.connect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Database client service unavailable. Application cannot start.",
        ) from e

    try:
        docker_client.connect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Docker client service unavailable. Application cannot start.",
        ) from e

    try:
        celery_client.connect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Celery client service unavailable. Application cannot start.",
        ) from e

    try:
        redis_client.connect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Celery client service unavailable. Application cannot start.",
        ) from e


@app.on_event("shutdown")
async def shutdown_event():
    try:
        db_client.disconnect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Celery client service unavailable.",
        ) from e

    try:
        docker_client.disconnect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Docker client service unavailable.",
        ) from e

    try:
        celery_client.disconnect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Celery client service unavailable.",
        ) from e

    try:
        redis_client.disconnect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error: Celery client service unavailable.",
        ) from e


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={
            "status_code": "422",
            "detail": f"Error: Unprocessable Entity",
        },
        status_code=422,
    )

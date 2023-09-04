# Purpose: Main file and entry point of the application
# Path: backend\app\main.py

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import files, transcriptions
from app.utils.docker_client import docker_client

# from app.utils.redis_client import redis_client

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


@app.on_event("startup")
async def startup_event():
    if not docker_client.ping():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Docker client service unavailable. Application cannot start.",
        )

    # if not redis_client.ping():
    #     raise HTTPException(
    #         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #         detail="Redis connection not established. Application cannot start.",
    #     )


@app.on_event("shutdown")
async def shutdown_event():
    try:
        docker_client.disconnect()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Docker client service unavailable.",
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

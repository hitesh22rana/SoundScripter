# Purpose: Environment configuration for the application.
# Path: backend\app\config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    worker_concurrency: int
    celery_backend: str
    celery_broker: str
    local_storage_base_path: str
    redis_host: str
    redis_port: int
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_port: int

    class Config:
        env_file = ".env"


settings = Settings()

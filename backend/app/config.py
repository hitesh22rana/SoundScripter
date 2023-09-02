# Purpose: Environment configuration for the application.
# Path: backend\app\config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_concurrent_containers: int

    class Config:
        env_file = ".env"


settings = Settings()

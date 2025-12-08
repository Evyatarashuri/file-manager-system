from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_ID: str
    FIREBASE_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    STORAGE_BUCKET: str = "file-manager-assets"
    PUBSUB_FILE_UPLOADED_TOPIC: str = "file-uploaded"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

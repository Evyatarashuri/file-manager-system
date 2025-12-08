from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_ID: str = "eighth-epigram-434908-k0-63b90"
    FIREBASE_PROJECT_ID: str = "eighth-epigram-434908-k0-63b90"
    PUBSUB_FILE_UPLOADED_SUB: str = "file-uploaded-sub"
    GOOGLE_APPLICATION_CREDENTIALS: str = "/app/service-accounts/worker-sa.json"
    STORAGE_BUCKET: str = "file-manager-assets"
    PUBSUB_FILE_UPLOADED_TOPIC: str = "file-uploaded"
    REDIS_URL: str = "redis://10.90.0.3:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

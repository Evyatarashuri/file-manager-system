from google.cloud import storage
from logging import getLogger
from app.config.settings import settings
from datetime import datetime, timedelta, timezone

logger = getLogger("storage-repo")

class StorageRepo:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.STORAGE_BUCKET)

    def upload_file(self, path: str, upload_file):
        logger.info(f"Uploading → {path}")
        blob = self.bucket.blob(path)
        blob.upload_from_file(upload_file.file, content_type=upload_file.content_type)
        logger.info(f"File uploaded successfully to Storage: {path}")
        return True

    def download_file(self, path: str):
        blob = self.bucket.blob(path)
        return blob.download_as_bytes()

    def delete_file(self, path: str):
        blob = self.bucket.blob(path)
        blob.delete()
        return True
    
    def generate_signed_url(self, path: str, expiration=3600) -> str:
        blob = self.bucket.blob(path)

        return blob.generate_signed_url(
            expiration=datetime.now(timezone.utc) + timedelta(seconds=expiration)
        )

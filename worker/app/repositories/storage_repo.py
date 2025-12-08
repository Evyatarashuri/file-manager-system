from google.cloud import storage
from google.api_core.exceptions import NotFound, ServiceUnavailable
from app.utils.backoff import backoff
from app.config.logging import get_logger
from app.config.settings import settings

logger = get_logger("worker-storage")


class StorageRepo:
    def __init__(self):
        bucket_name = settings.STORAGE_BUCKET
        if not bucket_name:
            raise RuntimeError("STORAGE_BUCKET not set")

        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        logger.info(f"Worker connected to bucket: {bucket_name}")


    @backoff(max_retries=5)
    def download_file(self, path: str) -> bytes:
        blob = self.bucket.blob(path)

        try:
            data = blob.download_as_bytes()
        except NotFound:
            logger.error(f"File not found in storage: {path}")
            return b""
        except ServiceUnavailable:
            logger.warning(f"GCS temporarily unavailable while fetching {path}")
            raise
        except Exception as e:
            logger.error(f"Unhandled error while downloading {path}: {e}")
            raise

        if not data:
            logger.warning(f"Downloaded empty file: {path}")

        logger.info(f"Downloaded {len(data)} bytes from {path}")
        return data

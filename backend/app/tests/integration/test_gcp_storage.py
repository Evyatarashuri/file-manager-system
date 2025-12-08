import uuid
import pytest
from google.cloud import storage
from app.config.settings import settings

@pytest.mark.integration
def test_storage_upload_and_download():
    client = storage.Client(project=settings.PROJECT_ID)
    bucket = client.bucket(settings.STORAGE_BUCKET)

    test_path = f"tests/{uuid.uuid4()}.txt"
    blob = bucket.blob(test_path)

    data = b"File storage test works!"
    blob.upload_from_string(data)

    downloaded = blob.download_as_bytes()
    assert downloaded == data, "Storage upload/download mismatch"

    blob.delete()
    print("Storage OK – upload/download/delete successful")

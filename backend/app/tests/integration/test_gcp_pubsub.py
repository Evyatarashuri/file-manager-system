import pytest
from google.cloud import pubsub_v1
from app.config.settings import settings

@pytest.mark.integration
def test_pubsub_publish():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.PROJECT_ID, settings.PUBSUB_FILE_UPLOADED_TOPIC)

    future = publisher.publish(topic_path, b"test_pubsub_message")
    result = future.result(timeout=10)

    assert result is not None, "Pub/Sub publish failed"
    print("Pub/Sub topic publish OK")

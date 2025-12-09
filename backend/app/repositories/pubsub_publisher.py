from google.cloud import pubsub_v1
import json
from app.config.settings import settings

class PubSubPublisher:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            settings.FIREBASE_PROJECT_ID, 
            settings.PUBSUB_FILE_UPLOADED_TOPIC
        )

    def publish_file_uploaded(self, file_id: str, user_id: str, storage_path: str, content_type: str):
        message = {
            "event": "FILE_UPLOADED",
            "file_id": file_id,
            "user_id": user_id,
            "storage_path": storage_path,
            "content_type": content_type
        }

        self.publisher.publish(
            self.topic_path,
            json.dumps(message).encode("utf-8")
        )
 
    # not in use for now - but could be useful later
    def publish_file_deleted(self, file_id: str, user_id: str):
        message = {
            "event": "FILE_DELETED",
            "file_id": file_id,
            "user_id": user_id
        }

        self.publisher.publish(
            self.topic_path,
            json.dumps(message).encode("utf-8")
        )

from google.cloud import firestore
from app.config.logging import get_logger

logger = get_logger("worker-firestore")

class FirestoreRepo:
    def __init__(self):
        self.db = firestore.Client()

    def update_file_index(self, file_id: str, user_id: str, index_doc: dict):
        doc_ref = self.db.collection("files").document(file_id)
        snap = doc_ref.get()

        if not snap.exists:
            logger.warning(f"File metadata not found for indexing: {file_id}")
            return

        existing = snap.to_dict()
        if existing.get("owner_id") != user_id:
            logger.warning(f"owner_id mismatch for file {file_id}")
            return

        doc_ref.set(index_doc, merge=True)
        logger.info(f"Index fields merged into file {file_id}")

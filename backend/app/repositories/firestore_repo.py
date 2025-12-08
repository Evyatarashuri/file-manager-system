from google.cloud import firestore
from app.middleware.logging import get_logger

logger = get_logger("FirestoreRepo")

class FirestoreRepo:
    def __init__(self):
        self.db = firestore.Client()

    # ---------------------------
    # File operations
    # ---------------------------
    def save_file_metadata(self, metadata: dict):
        file_id = metadata["file_id"]
        self.db.collection("files").document(file_id).set(metadata)

    def get_file_metadata(self, file_id: str):
        doc = self.db.collection("files").document(file_id).get()
        return doc.to_dict() if doc.exists else None

    def delete_file_metadata(self, file_id: str):
        self.db.collection("files").document(file_id).delete()

    def get_user_files(self, user_id: str):
        docs = (
            self.db.collection("files")
            .where("owner_id", "==", user_id)
            .stream()
        )
        return [doc.to_dict() for doc in docs]

    def get_all_files(self):
        docs = self.db.collection("files").stream()
        return [doc.to_dict() for doc in docs]

    # ---------------------------
    # Indexed search
    # ---------------------------
    def search_user_files(self, user_id: str, query: str):
        # This depends on worker adding "search_index" into Firestore
        docs = (
            self.db.collection("files")
            .where("owner_id", "==", user_id)
            .stream()
        )

        results = []
        for doc in docs:
            data = doc.to_dict()
            index = data.get("search_index", "").lower()

            if query.lower() in index:
                results.append(data)

        return results

    # ---------------------------
    # User preferences
    # ---------------------------
    def get_user_document(self, user_id: str):
        doc = self.db.collection("users").document(user_id).get()
        return doc.to_dict() if doc.exists else None

    def update_user_document(self, user_id: str, data: dict):
        self.db.collection("users").document(user_id).set(data, merge=True)


    def get_file(self, file_id: str) -> dict | None:
        doc = self.db.collection("files").document(file_id).get()
        return doc.to_dict() if doc.exists else None

    def delete_file(self, file_id: str):
        logger.info(f"Deleting file: {file_id}")
        return self.db.collection("files").document(file_id).delete()
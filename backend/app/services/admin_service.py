from app.repositories.firestore_repo import FirestoreRepo
from app.middleware.logging import get_logger

logger = get_logger("AdminService")

class AdminService:
    def __init__(self):
        self.firestore = FirestoreRepo()

    def get_all_files(self):
        logger.info("Admin fetching ALL files in the system")
        return self.firestore.get_all_files()

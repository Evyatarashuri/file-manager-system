from app.repositories.firestore_repo import FirestoreRepo
from datetime import datetime, timezone

class AuditService:
    def __init__(self):
        self.db = FirestoreRepo()

    def log_action(self, user_id: str, action: str, file_id: str | None = None, meta: dict = None):
        data = {
            "user_id": user_id,
            "action": action,
            "file_id": file_id,
            "meta": meta or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.db.save_audit_log(data)
        print(f"Audit → {action} user={user_id} file={file_id}")
        return data

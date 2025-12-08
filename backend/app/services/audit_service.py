from datetime import datetime, timezone
from google.cloud import firestore

class AuditService:
    def __init__(self):
        self.db = firestore.Client()

    def audit_event(self, event_type: str, user_id: str, details: dict):
        """Write audit logs to Firestore"""
        try:
            entry = {
                "event": event_type,
                "user_id": user_id,
                "details": details,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            self.db.collection("audit_logs").add(entry)

            print(f"AUDIT LOG — {event_type} | {user_id} → {details}")

        except Exception as e:
            print(f"AUDIT WRITE FAILED: {e}")

# Singleton instance
audit_service = AuditService()

# Used externally
def audit_event(event_type, user_id, details):
    return audit_service.audit_event(event_type, user_id, details)

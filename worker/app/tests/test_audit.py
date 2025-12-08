from app.services.audit_service import AuditService

def test_audit_log(monkeypatch):
    svc = AuditService()

    recorded = []
    monkeypatch.setattr(svc.db, "save_audit_log", lambda data: recorded.append(data))

    svc.log_action("u123","FILE_UPLOAD","file99")

    assert recorded[0]["action"] == "FILE_UPLOAD"
    assert recorded[0]["file_id"] == "file99"

import uuid
import pytest
from google.cloud import firestore
from app.config.settings import settings

@pytest.mark.integration
def test_firestore_connectivity():
    db = firestore.Client(project=settings.PROJECT_ID)

    test_id = f"test-{uuid.uuid4()}"
    ref = db.collection("tests").document(test_id)

    ref.set({"ok": True})
    doc = ref.get()

    assert doc.exists, "Firestore did not save document"
    assert doc.to_dict()["ok"] is True

    ref.delete()
    assert not ref.get().exists

    print("Firestore Connectivity OK")

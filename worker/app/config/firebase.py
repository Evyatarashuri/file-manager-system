import os, firebase_admin
from firebase_admin import credentials
from app.config.logging import get_logger

logger = get_logger("firebase_config-worker")

cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Cloud Run (Secret Manager injects file) OR local file-based credential
if cred_path and os.path.exists(cred_path):
    firebase_admin.initialize_app(credentials.Certificate(cred_path))
    logger.info("Firebase Admin initialized from GOOGLE_APPLICATION_CREDENTIALS")
else:
    logger.warning("Firebase Admin NOT initialized — no credentials detected")

import firebase_admin
from firebase_admin import credentials
import os
from app.middleware.logging import get_logger

logger = get_logger("firebase-config")

def init_firebase():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not cred_path or not os.path.exists(cred_path):
        logger.error(f"Firebase credential file missing at path: {cred_path}")
        raise RuntimeError("Firebase credentials missing")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(cred_path))
        logger.info("Firebase initialized successfully")


# initialize on startup
init_firebase()

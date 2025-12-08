import logging
from datetime import datetime, timezone

logger = logging.getLogger("audit")

def audit(action: str, user_id: str, metadata: dict = None):
    entry = {
        "action": action,
        "user_id": user_id,
        "metadata": metadata or {},
        "timestamp": datetime.now(timezone.utc)
    }

    # structured log
    logger.info(entry)

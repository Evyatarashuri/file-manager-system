from fastapi import Depends, HTTPException, Header
from firebase_admin import auth
from app.middleware.logging import get_logger

logger = get_logger("auth-debug")

async def verify_firebase_token(authorization: str = Header(None)):
    logger.info(f"Incoming Auth Header: {authorization}")

    if not authorization or not authorization.startswith("Bearer "):
        logger.error(f"No token in Authorization header")
        raise HTTPException(status_code=401, detail="Authorization token missing")

    token = authorization.split("Bearer ")[1]

    try:
        decoded = auth.verify_id_token(token)
        logger.info(f"Firebase token verified")
        return decoded

    except Exception as e:
        logger.error(f"Token invalid: {e}")
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")

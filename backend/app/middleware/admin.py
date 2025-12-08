from fastapi import Depends, HTTPException
from app.middleware.auth import verify_firebase_token
from app.middleware.logging import get_logger

logger = get_logger("admin-middleware")

async def require_admin(user=Depends(verify_firebase_token)):
    if not user.get("admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
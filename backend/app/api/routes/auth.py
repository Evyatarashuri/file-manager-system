from fastapi import APIRouter, Depends
from app.middleware.auth import verify_firebase_token

router = APIRouter()

@router.get("/me")
async def get_me(user=Depends(verify_firebase_token)):
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "name": user.get("name"),
        "picture": user.get("picture"),
    }

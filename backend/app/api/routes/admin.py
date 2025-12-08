from fastapi import APIRouter, Depends
from app.middleware.admin import require_admin
from app.services.admin_service import AdminService
from app.middleware.audit import audit

router = APIRouter(tags=["Admin"])
admin_service = AdminService()

@router.get("/all")
async def get_all_files(admin = Depends(require_admin)):
    audit("ADMIN_VIEW_ALL_FILES", admin["uid"], {})
    return admin_service.get_all_files()

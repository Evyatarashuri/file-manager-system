from fastapi import APIRouter, Request, UploadFile, File, Depends, HTTPException, status
from app.middleware.auth import verify_firebase_token
from app.services.file_service import FileService
from app.services.audit_service import audit_event
from app.middleware.logging import get_logger
from app.utils.idempotency import idempotent

router = APIRouter(tags=["Files"])
file_service = FileService()
logger = get_logger("files")


# ==========================================
#  Upload File (secured by Firebase Auth)
# ==========================================
@router.post("/upload", status_code=status.HTTP_201_CREATED)
@idempotent
async def upload_files(
    request: Request,
    files: list[UploadFile] = File(...),
    user: dict = Depends(verify_firebase_token)
):
    logger.info("UPLOAD REQUEST RECEIVED")
    logger.info(f"User Verified: {user['uid']}")
    logger.info(f"Received {len(files)} file(s)")

    audit_event("UPLOAD_ATTEMPT", user["uid"], {"count": len(files)})

    try:
        results = await file_service.handle_upload(files, user)

        audit_event("UPLOAD_SUCCESS", user["uid"], {"uploaded": len(results)})

        return {
            "status": "success",
            "uploaded_files": results,
            "count": len(results),
            "message": "Files uploaded and events published to Pub/Sub"
            }

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        audit_event("UPLOAD_FAILED", user["uid"], {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
#  Get user files list
# ==========================================
@router.get("/")
async def list_user_files(
    user=Depends(verify_firebase_token),
    sort_by: str | None = None,
    file_type: str | None = None,
    search: str | None = None,
):
    logger.info(f"Listing files for user: {user['uid']}")
    
    if not sort_by and not file_type and not search:
        logger.info("No filters applied, fetching all files.")
        return file_service.list_files_filtered(user["uid"])

    return file_service.list_files_filtered(
        user_id=user["uid"],
        sort_by=sort_by,
        file_type=file_type,
        search=search
    )

# ==========================================
#  Get specific file metadata
# ==========================================
@router.get("/{file_id}")
async def get_file(file_id: str, user=Depends(verify_firebase_token)):
    try:
        logger.info(f"Fetching file {file_id} for user {user['uid']}")
        return file_service.get_file(file_id, user["uid"])
    except Exception as e:
        logger.error(f"Error fetching file {file_id} for user {user['uid']}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ==========================================
#  Delete File
# ==========================================
@router.delete("/{file_id}")
async def delete_file(file_id: str, user=Depends(verify_firebase_token)):
    audit_event("DELETE_ATTEMPT", user["uid"], {"file_id": file_id})

    deleted = file_service.delete_file(file_id, user["uid"])

    if not deleted:
        audit_event("DELETE_FORBIDDEN", user["uid"], {"file_id": file_id})
        raise HTTPException(status_code=403, detail="Not allowed to delete this file")

    audit_event("DELETE_SUCCESS", user["uid"], {"file_id": file_id})
    return {"deleted": True}


# ==========================================
#  Download File
# ==========================================
@router.get("/download/{file_id}")
async def download_file(file_id: str, user=Depends(verify_firebase_token)):
    file = file_service.get_file(file_id, user["uid"])
    if not file:
        logger.warning(f"File not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")

    signed_url = file_service.get_download_url(file)
    if not signed_url:
        logger.error(f"Failed to generate signed URL for file: {file_id}")
        audit_event("DOWNLOAD_FAILED", user["uid"], {"file_id": file_id})
        raise HTTPException(status_code=500, detail="Could not generate download URL")
    return {"url": signed_url}
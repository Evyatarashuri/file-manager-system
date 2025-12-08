from datetime import datetime, timezone
import uuid
from fastapi import UploadFile, HTTPException
from app.repositories.firestore_repo import FirestoreRepo
from app.repositories.storage_repo import StorageRepo
from app.repositories.pubsub_publisher import PubSubPublisher
from app.schemas.file_schema import FileMetadata
from app.middleware.logging import get_logger

logger = get_logger("FileService")

class FileService:
    def __init__(self):
        self.firestore = FirestoreRepo()
        self.storage = StorageRepo()
        self.publisher = PubSubPublisher()
    
    def _serialize(self, metadata: dict):
        for k, v in metadata.items():
            if isinstance(v, datetime):
                metadata[k] = v.isoformat()
        return metadata

    # ===========================================================
    # UPLOAD FILES (Already implemented)
    # ===========================================================
    async def handle_upload(self, files: list[UploadFile], user: dict):
        logger.info(f"Handling upload for user: {user['uid']}")
        user_id = user["uid"]
        uploaded = []

        for file in files:

            if not (
                file.content_type.startswith("application/pdf")
                or file.content_type in ["application/json", "text/plain"]
            ):
                logger.error(f"Unsupported file type: {file.content_type}")
                raise HTTPException(400, f"Unsupported file type: {file.content_type}")

            file_id = str(uuid.uuid4())
            storage_path = f"user_files/{user_id}/{file_id}"
            
            logger.info(f"Uploading file {file.filename} to {storage_path}")
            self.storage.upload_file(storage_path, file)

            file.file.seek(0, 2)
            size = file.file.tell()
            file.file.seek(0)

            metadata = FileMetadata(
                file_id=file_id,
                owner_id=user_id,
                owner_email=user.get("email"),
                filename=file.filename,
                content_type=file.content_type,
                storage_path=storage_path,
                size=size,
                uploaded_at=datetime.now(timezone.utc)
            ).model_dump()

            self.firestore.save_file_metadata(metadata)
            logger.info(f"Saved metadata for Firestore: {file_id}")


            self.publisher.publish_file_uploaded(
                file_id=file_id,
                user_id=user_id,
                storage_path=storage_path,
                content_type=file.content_type
            )
            logger.info(f"Published upload event for PubSub file: {file_id}")

            uploaded.append(self._serialize(metadata))

        return uploaded

    # ===========================================================
    # MAIN FILE LIST WITH SEARCH + FILTER + SORT
    # ===========================================================
    def list_files_filtered(
        self,
        user_id: str,
        sort_by: str | None = None,
        file_type: str | None = None,
        search: str | None = None
    ):
        logger.info(f"Listing files for user: {user_id}")
        files = self.firestore.get_user_files(user_id)

        # Search
        if search:
            logger.info(f"Searching files for user: {user_id} with query: {search}")
            files = [f for f in files if search.lower() in f.get("filename","").lower()]

        # Filter by file type (pdf/txt/json)
        if file_type:
            logger.info(f"Filtering files for user: {user_id} by type: {file_type}")
            files = [f for f in files if f.get("content_type","").endswith(file_type)]

        # ↕ Sort (date or size)
        if sort_by == "date":
            logger.info(f"Sorting files for user: {user_id} by date")
            files = sorted(files, key=lambda x: (x.get("uploaded_at") or ""), reverse=True)
        
        elif sort_by == "size":
            logger.info(f"Sorting files for user: {user_id} by size")
            files = sorted(files, key=lambda x: (x.get("size") or 0), reverse=True)

        return [self._serialize(f) for f in files]
    
    # ===========================================================
    # Single File Meta
    # ===========================================================
    def get_file(self, file_id, user_id):
        logger.info(f"Retrieving file metadata for user: {user_id}, file_id: {file_id}")
        file = self.firestore.get_file(file_id)
        if not file or file.get("owner_id") != user_id:
            return None
        return self._serialize(file)
    
    # ===========================================================
    # Delete
    # ===========================================================
    def delete_file(self, file_id, user_id):
        logger.info(f"Attempting to delete file for user: {user_id}, file_id: {file_id}")
        file = self.firestore.get_file(file_id)
        if not file or file.get("owner_id") != user_id:
            logger.warning(f"Delete file failed: {file_id} not found or access denied")
            return False

        self.storage.delete_file(file["storage_path"])
        self.firestore.delete_file(file_id)

        # Optional: publish deletion event
        # self.publisher.publish_file_deleted(file_id=file_id, user_id=user_id)

        return True
    
    # ===========================================================
    # Download Signed URL
    # ===========================================================
    def get_download_url(self, file_meta: dict) -> str:
        logger.info(f"Generating download URL for file: {file_meta['file_id']}")
        return self.storage.generate_signed_url(
            file_meta["storage_path"],
            expiration=3600  # 1 hour
        )

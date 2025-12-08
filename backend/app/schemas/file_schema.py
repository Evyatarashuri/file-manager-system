from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

class FileMetadata(BaseModel):
    file_id: str
    owner_id: str
    owner_email: Optional[str] = None
    filename: str
    content_type: str
    storage_path: str
    size: Optional[int] = None
    indexed: bool = False
    search_index: Optional[str] = None
    search_text: Optional[str] = None
    uploaded_at: datetime = datetime.now(timezone.utc)

    class Config:
        orm_mode = True

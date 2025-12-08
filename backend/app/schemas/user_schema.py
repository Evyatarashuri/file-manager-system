from pydantic import BaseModel
from typing import Optional

class UserPreferences(BaseModel):
    theme: Optional[str] = "light"
    sort_by: Optional[str] = "uploaded_at"
    view_mode: Optional[str] = "grid"

class UserData(BaseModel):
    uid: str
    email: str
    preferences: UserPreferences = UserPreferences()

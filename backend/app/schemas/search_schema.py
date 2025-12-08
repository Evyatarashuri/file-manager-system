from pydantic import BaseModel
from typing import List, Optional

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    file_id: str
    filename: str
    snippet: Optional[str]
    score: float = 1.0  # future expansion

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int

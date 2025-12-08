from fastapi import APIRouter, Depends, Query
from app.middleware.auth import verify_firebase_token
from app.schemas.search_schema import SearchResponse, SearchResult
from app.services.search_service import SearchService
from app.middleware.logging import get_logger

logger = get_logger("backend-search-api")

router = APIRouter(tags=["Search"])
search_service = SearchService()


@router.get("/", response_model=SearchResponse)
async def search_files(
    q: str = Query(..., description="Text search inside user files"),
    user=Depends(verify_firebase_token)
):
    logger.info("Starting search in user files")

    results = search_service.search_user_files(user["uid"], q)

    formatted = [
        SearchResult(
            file_id=f["file_id"],
            filename=f["filename"],
            snippet=_extract_snippet(
                (f.get("search_index") or {}).get("preview", ""),
                q
            ),
        )
        for f in results
    ]

    logger.info(f"Search-api completed for user_id={user['uid']} query={q}")
    return SearchResponse(results=formatted, total=len(formatted))


def _extract_snippet(text: str, query: str, window: int = 60):
    if not text:
        return None

    text = text.lower()
    idx = text.find(query.lower())

    if idx == -1:
        return None

    start = max(idx - window, 0)
    end = idx + window

    return text[start:end] + "..."


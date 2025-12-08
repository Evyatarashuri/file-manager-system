from app.repositories.firestore_repo import FirestoreRepo
from app.middleware.logging import get_logger

logger = get_logger("backend-search")

class SearchService:
    def __init__(self):
        self.firestore = FirestoreRepo()

    # -----------------------------------
    # Full-Text Search inside files
    # -----------------------------------
    def search_user_files(self, user_id: str, query: str):
        logger.info(f"Searching user files: user_id={user_id} query={query}")

        docs = (
            self.firestore.db.collection("files")
            .where("owner_id", "==", user_id)
            .stream()
        )

        results = []
        query = query.lower()

        for doc in docs:
            data = doc.to_dict()

            index = data.get("search_index", {})
            if not index:
                continue # skip non-indexed files

            terms = index.get("terms", [])

            # match relevance score
            score = sum(1 for t in terms if query in t)

            if score > 0:
                results.append({**data, "score": score})
        
        # sort most relevant first
        results.sort(key=lambda x: x["score"], reverse=True)

        logger.info(f"Search found {len(results)} results for user_id={user_id} query={query}")

        return results

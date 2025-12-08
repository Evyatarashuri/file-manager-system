from app.repositories.firestore_repo import FirestoreRepo

class SearchService:
    def __init__(self):
        self.db = FirestoreRepo()

    def search(self, user_id: str, query: str):
        query = query.lower()

        files = self.db.get_all_user_files(user_id)
        results = []

        for f in files:
            index = f.get("search_index", {})
            tokens = index.get("terms", [])

            if query in tokens:
                score = index["freq"].get(query, 0)
                results.append({
                    "file_id": f["id"],
                    "score": score,
                    "preview": index.get("preview")
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)

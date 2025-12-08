from app.services.search_index_builder import SearchService

def test_search_ranks_results(monkeypatch):
    svc = SearchService()

    monkeypatch.setattr(svc.db, "get_all_user_files", lambda uid: [
        {"id": "A", "search_index": {"terms": ["fast", "api"], "freq": {"fast":4}, "preview":"..."}},
        {"id": "B", "search_index": {"terms": ["fast"], "freq": {"fast":1}, "preview":"..."}}
    ])

    result = svc.search("U","fast")

    assert result[0]["file_id"] == "A"
    assert result[0]["score"] == 4

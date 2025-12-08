from app.services.indexing_service import IndexingService

def test_tokenizer_normalizes_and_splits():
    svc = IndexingService()
    tokens = svc.tokenize("Hello!! This, is a Test Test 123.")
    assert "hello" in tokens and "test" in tokens and "123" in tokens

def test_build_index_structure():
    svc = IndexingService()
    index = svc.build_search_index("apple banana apple orange")
    assert index["freq"]["apple"] == 2
    assert index["unique_terms"] == 3

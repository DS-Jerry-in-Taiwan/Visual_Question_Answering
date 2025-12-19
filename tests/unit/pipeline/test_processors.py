from src.pipeline.processors import QueryProcessor, ResultProcessor

def test_clean_query():
    qp = QueryProcessor()
    assert qp.clean_query("  test  ") == "test"
    assert qp.clean_query("\nquery\n") == "query"

def test_deduplicate():
    qp = QueryProcessor()
    queries = ["a", "b", "a", "c"]
    assert qp.deduplicate(queries) == ["a", "b", "c"]

def test_filter_results():
    rp = ResultProcessor()
    results = [
        {"id": "1", "score": 0.9, "content": "A"},
        {"id": "2", "score": 0.5, "content": "B"},
        {"id": "3", "score": 0.3, "content": "C"},
    ]
    filtered = rp.filter_results(results, threshold=0.6)
    assert filtered == [{"id": "1", "score": 0.9, "content": "A"}]

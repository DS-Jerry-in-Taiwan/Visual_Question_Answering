import pytest
from src.retrieval.models import RetrievalResult, RetrievalQuery
from datetime import datetime

def test_retrieval_result_valid():
    result = RetrievalResult(id="1", score=0.8, content="測試內容")
    assert result.id == "1"
    assert result.score == 0.8
    assert result.content == "測試內容"

def test_retrieval_result_invalid_score():
    with pytest.raises(ValueError):
        RetrievalResult(id="1", score=1.5, content="測試內容")

def test_retrieval_result_missing_id():
    with pytest.raises(ValueError):
        RetrievalResult(id="", score=0.5, content="測試內容")

def test_retrieval_result_missing_content():
    with pytest.raises(ValueError):
        RetrievalResult(id="1", score=0.5, content="")

def test_retrieval_result_to_dict():
    dt = datetime(2025, 12, 18, 3, 0, 0)
    result = RetrievalResult(id="1", score=0.9, content="內容", metadata={"a": 1}, timestamp=dt)
    d = result.to_dict()
    assert d["id"] == "1"
    assert d["score"] == 0.9
    assert d["content"] == "內容"
    assert d["metadata"] == {"a": 1}
    assert d["timestamp"] == dt.isoformat()

def test_retrieval_query_valid():
    q = RetrievalQuery(query="查詢", top_k=10, threshold=0.7)
    assert q.query == "查詢"
    assert q.top_k == 10
    assert q.threshold == 0.7

def test_retrieval_query_invalid_top_k():
    with pytest.raises(ValueError):
        RetrievalQuery(query="查詢", top_k=0)

def test_retrieval_query_invalid_threshold():
    with pytest.raises(ValueError):
        RetrievalQuery(query="查詢", threshold=1.5)

def test_retrieval_query_empty_query():
    with pytest.raises(ValueError):
        RetrievalQuery(query="   ")

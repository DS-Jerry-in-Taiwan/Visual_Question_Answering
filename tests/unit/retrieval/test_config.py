import pytest
from src.retrieval.config import RetrievalConfig

def test_retrieval_config_env(monkeypatch):
    monkeypatch.setenv("VLM_RAG_ENDPOINT", "http://test-endpoint")
    monkeypatch.setenv("VLM_RAG_API_KEY", "test-key")
    config = RetrievalConfig()
    assert config.vlm_rag_endpoint == "http://test-endpoint"
    assert config.vlm_rag_api_key == "test-key"
    assert config.default_top_k == 5
    assert config.timeout_seconds == 10

from pydantic_core import ValidationError

def test_retrieval_config_invalid(monkeypatch):
    monkeypatch.delenv("VLM_RAG_ENDPOINT", raising=False)
    monkeypatch.delenv("VLM_RAG_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        RetrievalConfig()

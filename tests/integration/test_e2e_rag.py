import pytest
import asyncio
from unittest.mock import AsyncMock
from src.e2e.rag_pipeline import E2ERAGPipeline
from src.pipeline.query_pipeline import QueryPipeline
from src.llm.client import LLMClient
from src.llm.config import LLMConfig

@pytest.mark.asyncio
async def test_e2e_rag_full_flow():
    # Mock QueryPipeline
    mock_query_pipeline = AsyncMock()
    mock_query_pipeline.process = AsyncMock(return_value={
        "formatted_context": "Context for: E2E 測試查詢",
        "results": [
            {"id": "1", "score": 0.9, "content": "A"},
            {"id": "2", "score": 0.7, "content": "B"}
        ],
        "metadata": {"top_k": 5}
    })
    llm_config = LLMConfig(api_key="test_key")
    llm_client = LLMClient(llm_config)
    pipeline = E2ERAGPipeline(mock_query_pipeline, llm_client)
    result = await pipeline.query("E2E 測試查詢")
    assert "answer" in result
    assert "context" in result
    assert "retrieval_results" in result
    assert "metadata" in result
    assert result["context"].startswith("Context for:")
    assert result["answer"].startswith("LLM response for:")
    assert len(result["retrieval_results"]) == 2
    assert result["metadata"]["top_k"] == 5

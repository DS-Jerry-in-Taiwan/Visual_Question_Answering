import pytest
from unittest.mock import AsyncMock
from src.pipeline.query_pipeline import QueryPipeline
from src.pipeline.config import PipelineConfig

@pytest.mark.asyncio
async def test_query_pipeline_basic_init_and_process():
    mock_client = AsyncMock()
    mock_client.search = AsyncMock(return_value=[{"id": "1", "score": 0.9, "content": "內容"}])
    pipeline = QueryPipeline(mock_client, PipelineConfig())
    result = await pipeline.process("測試查詢")
    assert "formatted_context" in result
    assert "results" in result
    assert "metadata" in result
    assert result["results"][0]["id"] == "1"

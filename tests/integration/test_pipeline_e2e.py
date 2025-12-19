import pytest
from unittest.mock import AsyncMock
from src.pipeline.query_pipeline import QueryPipeline
from src.pipeline.config import PipelineConfig
from src.pipeline.processors import ResultProcessor
from src.pipeline.formatters import ContextFormatter

@pytest.mark.asyncio
async def test_pipeline_e2e_basic():
    # Mock RetrievalClient
    mock_client = AsyncMock()
    mock_client.search = AsyncMock(return_value=[
        {"id": "1", "score": 0.9, "content": "A"},
        {"id": "2", "score": 0.7, "content": "B"},
        {"id": "3", "score": 0.5, "content": "C"},
    ])
    config = PipelineConfig()
    pipeline = QueryPipeline(mock_client, config)
    processor = ResultProcessor()
    formatter = ContextFormatter()

    # Simulate pipeline process
    query = "整合測試查詢"
    result = await pipeline.process(query)
    filtered = processor.filter_results(result["results"], threshold=0.7)
    formatted = formatter.format_for_llm(query, filtered)

    assert "formatted_context" in result
    assert "results" in result
    assert "metadata" in result
    assert len(filtered) == 2
    assert "- [0.90] A" in formatted
    assert "- [0.70] B" in formatted

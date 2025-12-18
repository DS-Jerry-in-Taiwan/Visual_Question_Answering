import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.retrieval.client import RetrievalClient
from src.retrieval.config import RetrievalConfig
from src.retrieval.models import RetrievalResult

@pytest.mark.asyncio
async def test_search_success():
    config = RetrievalConfig(
        vlm_rag_endpoint="http://test.com",
        vlm_rag_api_key="test_key"
    )
    mock_response = {
        "results": [{"id": "1", "score": 0.9, "content": "內容"}]
    }
    async with RetrievalClient(config) as client:
        with patch.object(client, '_retry_with_backoff', new=AsyncMock(return_value=mock_response)):
            results = await client.search("測試")
            assert len(results) == 1
            assert isinstance(results[0], RetrievalResult)
            assert results[0].id == "1"

@pytest.mark.asyncio
async def test_search_timeout():
    config = RetrievalConfig(
        vlm_rag_endpoint="http://test.com",
        vlm_rag_api_key="test_key"
    )
    async with RetrievalClient(config) as client:
        with patch.object(client, '_retry_with_backoff', side_effect=asyncio.TimeoutError()):
            results = await client.search("測試")
            assert results == []

@pytest.mark.asyncio
async def test_health_check_success():
    config = RetrievalConfig(
        vlm_rag_endpoint="http://test.com/api/search",
        vlm_rag_api_key="test_key"
    )
    async with RetrievalClient(config) as client:
        with patch.object(client.session, 'get', new=AsyncMock()) as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 200
            healthy = await client.health_check()
            assert healthy

@pytest.mark.asyncio
async def test_health_check_fail():
    config = RetrievalConfig(
        vlm_rag_endpoint="http://test.com/api/search",
        vlm_rag_api_key="test_key"
    )
    async with RetrievalClient(config) as client:
        with patch.object(client.session, 'get', new=AsyncMock(side_effect=Exception("fail"))):
            healthy = await client.health_check()
            assert not healthy

@pytest.mark.asyncio
async def test_search_api_error():
    config = RetrievalConfig(
        vlm_rag_endpoint="http://test.com",
        vlm_rag_api_key="test_key"
    )
    async with RetrievalClient(config) as client:
        with patch.object(client, '_retry_with_backoff', side_effect=Exception("API error")):
            results = await client.search("測試")
            assert results == []

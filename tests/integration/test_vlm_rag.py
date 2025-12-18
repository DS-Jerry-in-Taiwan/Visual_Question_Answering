import pytest
import json
from pathlib import Path
import asyncio
from src.retrieval.client import RetrievalClient
from src.retrieval.config import RetrievalConfig

@pytest.mark.asyncio
async def test_retrieval_client_with_real_api():
    queries_file = Path("tests/data/rag_test_queries.json")
    queries = json.loads(queries_file.read_text())
    config = RetrievalConfig()
    async with RetrievalClient(config) as client:
        is_healthy = await client.health_check()
        assert is_healthy, "API health check failed"
        for query_data in queries[:5]:
            query_text = query_data["query"]
            video_id = query_data["video_id"]
            results = await client.search(query_text, video_id=video_id)
            assert isinstance(results, list)
            print(f"Query: {query_text} -> {len(results)} results")
            for result in results:
                assert result.id
                assert 0 <= result.score <= 1
                assert result.content

if __name__ == "__main__":
    asyncio.run(test_retrieval_client_with_real_api())

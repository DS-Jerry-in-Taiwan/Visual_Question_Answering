import pytest
import asyncio
from src.llm.config import LLMConfig
from src.llm.client import LLMClient

@pytest.mark.asyncio
async def test_llm_client_generate():
    config = LLMConfig(api_key="test_key")
    client = LLMClient(config)
    prompt = "請簡述 RAG 流程"
    result = await client.generate(prompt)
    assert "answer" in result
    assert result["answer"].startswith("LLM response for:")
    assert result["model"] == config.model
    assert result["provider"] == config.provider

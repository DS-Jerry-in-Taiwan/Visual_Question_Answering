import pytest
import asyncio
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src")))
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

import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))
from src.llm.config import LLMConfig
from src.llm.client import LLMClient

@pytest.mark.asyncio
async def test_llm_client_real_api():
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    assert api_key and api_key != "your-api-key-here", "請設置有效的 LLM_API_KEY 或 OPENAI_API_KEY"
    config = LLMConfig(api_key=api_key)
    client = LLMClient(config)
    context = [
        {"event_id": "evt001", "description": "12/30 15:00 大廳有人徘徊", "score": 0.82},
        {"event_id": "evt002", "description": "12/30 15:05 有人進入停車場", "score": 0.77},
    ]
    prompt = "請根據檢索事件回答：昨天下午大廳有異常活動嗎？"
    result = await client.generate(prompt, context=context)
    print("11111")
    print(result)
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert result["model"] == config.model
    assert result["provider"] == config.provider
    assert any("大廳" in result["answer"] or "異常" in result["answer"] for _ in [result])

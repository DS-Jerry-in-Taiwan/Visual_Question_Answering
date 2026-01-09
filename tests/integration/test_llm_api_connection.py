import os
import pytest

try:
    import openai
except ImportError:
    openai = None

@pytest.mark.skipif(openai is None, reason="openai package not installed")
def test_openai_api_key():
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    assert api_key and api_key != "your-api-key-here", "請設置有效的 LLM_API_KEY 或 OPENAI_API_KEY"

@pytest.mark.skipif(openai is None, reason="openai package not installed")
def test_openai_api_call():
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, world!"}],
        max_tokens=10,
    )
    assert "choices" in response
    assert response["choices"][0]["message"]["content"]

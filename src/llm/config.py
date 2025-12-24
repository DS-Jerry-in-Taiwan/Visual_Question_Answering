from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic import ConfigDict
from dotenv import load_dotenv
import os

# 確保 .env 會被自動載入
load_dotenv()

class LLMConfig(BaseSettings):
    model_config = ConfigDict(extra="allow")
    """LLM module configuration"""

    provider: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"), description="LLM provider name")
    api_key: str = Field(default_factory=lambda: os.getenv("LLM_API_KEY"), description="API key for LLM provider")
    model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-3.5-turbo"), description="Model name")
    timeout_seconds: int = Field(default_factory=lambda: int(os.getenv("LLM_TIMEOUT_SECONDS", 10)), ge=1, le=60)

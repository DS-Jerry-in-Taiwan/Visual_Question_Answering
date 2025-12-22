from pydantic_settings import BaseSettings
from pydantic import Field

class LLMConfig(BaseSettings):
    """LLM module configuration"""

    provider: str = Field("openai", description="LLM provider name")
    api_key: str = Field(..., description="API key for LLM provider")
    model: str = Field("gpt-3.5-turbo", description="Model name")
    timeout_seconds: int = Field(10, ge=1, le=60)

    class Config:
        env_file = ".env"

from pydantic_settings import BaseSettings
from pydantic import Field

class RetrievalConfig(BaseSettings):
    """檢索模組配置"""

    vlm_rag_endpoint: str = Field(..., env="VLM_RAG_ENDPOINT")
    vlm_rag_api_key: str = Field(..., env="VLM_RAG_API_KEY")

    default_top_k: int = Field(5, ge=1, le=100)
    default_threshold: float = Field(0.5, ge=0.0, le=1.0)
    timeout_seconds: int = Field(10, ge=1, le=60)

    max_retries: int = Field(3, ge=0, le=10)
    retry_base_delay: float = Field(1.0, ge=0.1)
    retry_max_delay: float = Field(10.0, ge=1.0)

    class Config:
        env_file = ".env"

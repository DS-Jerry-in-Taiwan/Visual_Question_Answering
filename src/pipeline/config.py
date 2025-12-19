from pydantic_settings import BaseSettings
from pydantic import Field


class PipelineConfig(BaseSettings):
    """Pipeline module configuration"""

    default_top_k: int = Field(5, ge=1, le=100)
    default_threshold: float = Field(0.5, ge=0.0, le=1.0)
    timeout_seconds: int = Field(10, ge=1, le=60)

    class Config:
        env_file = ".env"

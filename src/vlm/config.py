from pydantic_settings import BaseSettings
from pydantic import Field

class VLMConfig(BaseSettings):
    model_config = dict(extra="forbid")
    """VLM 模組設定"""
    model_name: str = Field("Qwen/Qwen2-VL-7B-Instruct", description="VLM 模型名稱")
    use_quantization: bool = Field(True, description="是否啟用 INT8 量化")
    max_frames: int = Field(4, ge=1, le=32, description="最大採樣幀數")
    device: str = Field("cuda", description="推理裝置")
    max_new_tokens: int = Field(512, description="最大生成 token 數")
    temperature: float = Field(0.7, description="生成溫度")
    do_sample: bool = Field(True, description="是否啟用隨機採樣")
    top_p: float = Field(0.95, description="top-p 採樣參數")

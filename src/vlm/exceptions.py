class VLMError(Exception):
    """VLM 模組基礎例外"""
    pass

class VideoReadError(VLMError):
    """影片讀取失敗"""
    pass

class ModelLoadError(VLMError):
    """模型載入失敗"""
    pass

class InferenceError(VLMError):
    """推理過程錯誤"""
    pass

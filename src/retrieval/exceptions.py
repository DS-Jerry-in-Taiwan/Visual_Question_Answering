class RetrievalError(Exception):
    """檢索模組基礎例外"""
    pass

class APIError(RetrievalError):
    """API 回應錯誤"""
    pass

class TimeoutError(RetrievalError):
    """API 請求超時"""
    pass

class ValidationError(RetrievalError):
    """資料驗證錯誤"""
    pass

class ConfigError(RetrievalError):
    """配置錯誤"""
    pass

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class RetrievalResult:
    """檢索結果"""
    id: str
    score: float
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if not 0 <= self.score <= 1:
            raise ValueError(f"Score must be 0-1, got {self.score}")
        if not self.id or not self.content:
            raise ValueError("ID and content required")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "score": self.score,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

@dataclass
class RetrievalQuery:
    """查詢參數"""
    query: str
    top_k: int = 5
    threshold: float = 0.5
    filters: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.query.strip():
            raise ValueError("Query cannot be empty")
        if self.top_k < 1:
            raise ValueError("top_k must be >= 1")
        if not 0 <= self.threshold <= 1:
            raise ValueError("threshold must be 0-1")

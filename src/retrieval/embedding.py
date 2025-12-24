from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingClient:
    """
    EmbeddingClient: 產生文本向量嵌入，支援 BGE-M3 等模型。
    """
    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model = SentenceTransformer(model_name)

    def embed_single(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def embed(self, texts: List[str]) -> List[List[float]]:
        return [self.model.encode(t).tolist() for t in texts]

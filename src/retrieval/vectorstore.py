import chromadb
from typing import List, Dict, Any

class ChromaVectorStore:
    """
    ChromaVectorStore: 基於 ChromaDB 的向量儲存與查詢。
    """
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], documents: List[str]):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def query(self, query_embeddings: List[List[float]], n_results: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        return results

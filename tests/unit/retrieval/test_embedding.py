from src.retrieval.embedding import EmbeddingClient

def test_embed_single():
    client = EmbeddingClient(model_name="sentence-transformers/all-MiniLM-L6-v2")
    text = "測試文本"
    embedding = client.embed_single(text)
    assert isinstance(embedding, list)
    assert len(embedding) > 0

def test_embed_batch():
    client = EmbeddingClient(model_name="sentence-transformers/all-MiniLM-L6-v2")
    texts = ["文本1", "文本2"]
    embeddings = client.embed(texts)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert all(isinstance(e, list) for e in embeddings)

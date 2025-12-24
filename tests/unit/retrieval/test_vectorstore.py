import tempfile
from src.retrieval.vectorstore import ChromaVectorStore

def test_add_and_query():
    temp_dir = tempfile.mkdtemp()
    store = ChromaVectorStore(persist_dir=temp_dir, collection_name="test_collection")
    ids = ["id1", "id2"]
    embeddings = [[0.1]*384, [0.2]*384]
    metadatas = [{"source": "test1"}, {"source": "test2"}]
    documents = ["doc1", "doc2"]
    store.add(ids, embeddings, metadatas, documents)
    results = store.query(query_embeddings=[[0.1]*384], n_results=2)
    assert "ids" in results
    assert len(results["ids"][0]) > 0

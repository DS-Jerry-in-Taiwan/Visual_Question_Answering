import json
from src.retrieval.embedding import EmbeddingClient
from src.retrieval.vectorstore import ChromaVectorStore

def main():
    # 讀取 output.json
    with open("output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    events = data["events"]

    # 初始化 embedding client 與 vector store
    embedder = EmbeddingClient()
    vectorstore = ChromaVectorStore(persist_dir="chroma_db", collection_name="event_index")

    # 批次處理所有事件摘要
    ids = []
    embeddings = []
    metadatas = []
    documents = []
    for evt in events:
        ids.append(evt["event_id"])
        documents.append(evt["summary"])
        metadatas.append({
            "segment_index": evt.get("segment_index"),
            "start_time": evt.get("start_time"),
            "end_time": evt.get("end_time"),
            "zone": evt.get("zone"),
            "activity": evt.get("activity"),
            "objects": ", ".join(evt.get("objects", [])) if isinstance(evt.get("objects"), list) else evt.get("objects"),
            "person_count": evt.get("person_count"),
            "confidence": evt.get("confidence"),
            "video_path": evt.get("video_path")
        })
    embeddings = embedder.embed(documents)

    # 寫入向量資料庫
    vectorstore.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
    print(f"已寫入 {len(ids)} 筆事件摘要至向量資料庫。")

if __name__ == "__main__":
    main()

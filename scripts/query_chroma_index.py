from src.retrieval.vectorstore import ChromaVectorStore

def main():
    vectorstore = ChromaVectorStore(persist_dir="chroma_db", collection_name="event_index")
    # 查詢全部資料（可用空向量查詢全部，或查詢前5筆）
    results = vectorstore.collection.get()
    print(f"資料庫內共有 {len(results['ids'])} 筆資料")
    for i, eid in enumerate(results['ids']):
        print(f"{i+1}. event_id: {eid}, summary: {results['documents'][i]}, metadata: {results['metadatas'][i]}")

if __name__ == "__main__":
    main()

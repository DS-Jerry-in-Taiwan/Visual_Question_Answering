import json
import asyncio
from src.llm.client import LLMClient
from src.llm.config import LLMConfig
from src.retrieval.embedding import EmbeddingClient
from src.retrieval.vectorstore import ChromaVectorStore

def main():
    # 載入 VLM 輸出
    with open("output.json", "r", encoding="utf-8") as f:
        vlm_output = json.load(f)
    # 可自定義查詢語句
    user_query = input("請輸入查詢語句：").strip()
    print(f"自定義查詢: {user_query}")

    # 本地 embedding & vectorstore 查詢
    embedder = EmbeddingClient()
    vectorstore = ChromaVectorStore(persist_dir="chroma_db", collection_name="event_index")
    query_vec = embedder.embed_single(user_query)
    results = vectorstore.query([query_vec], n_results=10)

    print("=== 本地檢索結果（含語意分數過濾）===")
    # 設定語意距離閾值，過濾不相關結果（如 0.5 以下才顯示）
    threshold = 0.5
    ids = results["ids"][0] if "ids" in results else []
    docs = results["documents"][0] if "documents" in results else []
    metas = results["metadatas"][0] if "metadatas" in results else []
    dists = results["distances"][0] if "distances" in results else []
    found = False
    filtered_docs = []
    for i in range(len(ids)):
        if dists[i] <= threshold:
            print(f"{i+1}. event_id: {ids[i]}, summary: {docs[i]}, metadata: {metas[i]}, distance: {dists[i]}")
            filtered_docs.append(str(docs[i]))
            found = True
    if not found:
        print(f"查無語意相關事件（距離 <= {threshold}）")

    # LLM 生成（僅有檢索結果時才執行）
    if filtered_docs:
        llm_client = LLMClient(LLMConfig())
        context = "\n".join(filtered_docs)
        # 若 generate 為 async coroutine，需同步呼叫
        if asyncio.iscoroutinefunction(llm_client.generate):
            llm_response = asyncio.run(llm_client.generate(context))
        else:
            llm_response = llm_client.generate(context)
        print("=== LLM Output ===")
        print("LLM Answer:", llm_response["answer"])
        print("Context:", context)
    else:
        print("=== LLM Output ===")
        print("無檢索結果，未進行 LLM 生成。")

if __name__ == "__main__":
    main()

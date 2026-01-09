from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.retrieval.embedding import EmbeddingClient
from src.retrieval.vectorstore import ChromaVectorStore
from src.llm.config import LLMConfig
from src.llm.client import LLMClient

import os
import json

from fastapi.staticfiles import StaticFiles
import cv2

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# 初始化嵌入模型與向量資料庫（可依需求調整路徑與 collection）
embedding_client = EmbeddingClient(model_name="BAAI/bge-m3")
vectorstore = ChromaVectorStore(
    persist_dir=os.getenv("CHROMA_DB_DIR", "chroma_db"),
    collection_name="event_index"
)

@app.post("/api/vqa")
async def vqa_query(request: Request):
    data = await request.json()
    query = data.get("query", "")
    print(f"[VQA_API] 查詢: {query}")
    # 1. 查詢語句 embedding
    query_emb = embedding_client.embed_single(query)
    # 2. 向量查詢
    results = vectorstore.query([query_emb], n_results=5)
    print(f"[VQA_API] 向量查詢結果: {results}")
    # 3. 組裝事件列表（僅回傳高於閾值的事件）
    threshold = float(os.getenv("RETRIEVAL_THRESHOLD", 0.5))
    events = []
    # results 可能為 list 或 dict，動態判斷
    if isinstance(results, dict):
        ids = results.get("ids", [])
        scores = results.get("distances", [])
        metadatas = results.get("metadatas", [])
        documents = results.get("documents", [])
    elif isinstance(results, list) and results:
        ids = results[0].get("ids", [])
        scores = results[0].get("distances", [])
        metadatas = results[0].get("metadatas", [])
        documents = results[0].get("documents", [])
    else:
        ids = []
        scores = []
        metadatas = []
        documents = []
    # 修正：展開二維陣列
    if ids and isinstance(ids[0], list):
        ids = ids[0]
    if scores and isinstance(scores[0], list):
        scores = scores[0]
    if metadatas and isinstance(metadatas[0], list):
        metadatas = metadatas[0]
    if documents and isinstance(documents[0], list):
        documents = documents[0]
    print(f"[VQA_API] threshold={threshold}, scores={scores}")
    def generate_snapshot(video_path, t):
        abs_path = os.path.join(os.getcwd(), video_path)
        cap = cv2.VideoCapture(abs_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_idx = int(float(t) * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return ""
        img_name = f"snapshot_{os.path.basename(video_path)}_{int(float(t))}.jpg"
        img_path = os.path.join("static", img_name)
        cv2.imwrite(img_path, frame)
        cap.release()
        return f"static/{img_name}"

    for i, eid in enumerate(ids):
        score = float(scores[i]) if i < len(scores) else 0
        meta = metadatas[i] if i < len(metadatas) else {}
        doc = documents[i] if i < len(documents) else ""
        # 強制型別一致再比較
        if score <= float(threshold):
            print(f"[VQA_API] event matched: score={score}, id={eid}")
            snapshot_url = ""
            video_path = meta.get("video_path", "")
            t = meta.get("start_time", "")
            if video_path and t != "":
                snapshot_url = generate_snapshot(video_path, t)
            events.append({
                "id": eid,
                "score": score,
                "description": doc or meta.get("summary", ""),
                "timestamp": meta.get("timestamp", ""),
                "video_path": video_path,
                "zone": meta.get("zone", ""),
                "activity": meta.get("activity", ""),
                "objects": meta.get("objects", ""),
                "person_count": meta.get("person_count", ""),
                "image_url": snapshot_url
            })
    print(f"[VQA_API] 組裝事件 events: {events}")
    # 4. 判斷是否有相關紀錄，若無則回傳提示
    if not events:
        print("[VQA_API] 查無相關事件紀錄，回傳預設訊息")
        return JSONResponse(content={
            "events": [],
            "answer": "查無相關事件紀錄，請嘗試其他查詢或確認資料庫內容。"
        })
    # 5. 串接 LLM 生成答案要求回傳格式
    prompt = (
        "請根據下列事件資料回答問題，只需直接給出最終結論與描述（不需摘要、不需事件列表），並以 JSON 格式回傳：\n"
        "{\n"
        '  "answer": "你的答案"\n'
        "}\n"
        f"事件資料：{events}\n"
        f"問題：{query}\n"
    )
    llm_config = LLMConfig()
    llm_client = LLMClient(llm_config)
    llm_result = await llm_client.generate(prompt=prompt, context=events)
    answer = llm_result.get("answer", "")
    print(f"[VQA_API] LLM 回答: {answer}")
    
    # 6. 解析 LLM 回傳的 JSON
    import re
    try:
        cleaned = re.sub(r"^```json|^```|```$", "", answer, flags=re.MULTILINE).strip()
        result = json.loads(cleaned)
        answer = result.get("answer", "")
        event_id = result.get("event_id", "")
    except Exception as e:
        print(f"[VQA_API] LLM 回傳格式錯誤: {e}")
        answer = llm_result.get("answer", "")
        event_id = ""
        
    # 7. 回傳前端
    print(f"[VQA_API] 回傳內容: events={len(events)}, answer={answer[:50]}")
    return JSONResponse(content={"events": events, "answer": answer, "event_id": event_id})

@app.post("/api/vqa/feedback")
async def vqa_feedback(request: Request):
    data = await request.json()
    print(f"收到回饋：{data}")
    return JSONResponse(content={"status": "ok", "msg": "回饋已記錄"})

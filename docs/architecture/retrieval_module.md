# Retrieval Module 設計

## 模組職責

Retrieval Module 負責與 VLM-RAG 系統對接，根據用戶查詢與影片資訊，檢索出最相關的影片片段、語意摘要與分數，並將結構化結果回傳給 Pipeline Module 或 API Module。

---

## 類別設計

### RetrievalClient 類別

```python
class RetrievalClient:
    def __init__(self, endpoint: str, api_key: str):
        ...

    def search(self, query: str, video_id: str, top_k: int = 5) -> List["RetrievalResult"]:
        """發送檢索請求，回傳檢索結果清單"""
        ...

    def parse_results(self, raw_response: dict) -> List["RetrievalResult"]:
        """解析 VLM-RAG 回傳的原始資料，轉為標準結構"""
        ...
```

---

## 資料模型

### RetrievalRequest

```python
class RetrievalRequest(BaseModel):
    query: str
    video_id: str
    top_k: int = 5
```

### RetrievalResult

```python
class RetrievalResult(BaseModel):
    segment_id: str
    score: float
    summary: str
```

---

## 錯誤處理策略

- 檢索服務異常（如連線失敗、超時）時，回傳預設錯誤訊息與空結果。
- 若 VLM-RAG 回傳格式異常，記錄日誌並回傳標準錯誤格式。
- 支援重試機制與降級策略（如回傳部分結果）。

---

## 使用範例

```python
client = RetrievalClient(endpoint="http://vlm-rag:8001", api_key="your_key")
req = RetrievalRequest(query="有無異常事件？", video_id="entrance_20231201", top_k=3)
results = client.search(req.query, req.video_id, req.top_k)
for r in results:
    print(r.segment_id, r.score, r.summary)
```

---

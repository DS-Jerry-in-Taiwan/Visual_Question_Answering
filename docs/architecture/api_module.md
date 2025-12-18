# API Module 設計

## 模組職責

API Module 基於 FastAPI，對外提供 RESTful API，負責路由設計、請求驗證、日誌記錄、錯誤處理與 CORS 設定，並串接 Pipeline、Retrieval、LLM 等核心模組。

---

## 路由設計（FastAPI）

- `POST /api/v1/query`：完整 VQA 查詢
- `POST /api/v1/retrieval/search`：檢索功能
- `POST /api/v1/llm/generate`：LLM 生成
- `GET /api/v1/health`：健康檢查
- `GET /api/v1/status`：狀態查詢

---

## 中介軟體

- **日誌記錄**：Loguru，記錄所有請求與錯誤
- **錯誤處理**：自訂 Exception Handler，統一錯誤格式
- **CORS 設定**：允許前端跨域請求

---

## 請求驗證（Pydantic）

- 所有請求/回應資料皆以 Pydantic Model 驗證
- 自動產生 OpenAPI 文件

---

## 使用範例

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    video_id: str
    top_k: int = 5

@app.post("/api/v1/query")
async def query_vqa(req: QueryRequest):
    # 呼叫 Pipeline 處理
    return {"answer": "示範答案"}

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
```

---

## 錯誤處理

- 統一回傳 JSON 格式錯誤訊息
- 支援 400/404/500 等狀態碼
- 所有異常皆記錄日誌

---

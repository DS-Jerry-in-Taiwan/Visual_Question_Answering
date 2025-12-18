# Visual_Question_Answering(VQA) API 規範

## API 概述

- **Base URL**: `/api/v1/`
- **版本管理**: 以 URL 前綴區分版本（如 `/api/v1/`）

---

## 端點列表

### 1. `POST /api/v1/query` - 完整 VQA 查詢
- 用戶提交查詢，系統自動完成檢索與生成，回傳答案。

### 2. `POST /api/v1/retrieval/search` - 檢索功能
- 直接呼叫檢索模組，回傳相關片段與語意資訊。

### 3. `POST /api/v1/llm/generate` - LLM 生成
- 直接呼叫 LLM 模組，根據輸入 prompt 生成答案。

### 4. `GET /api/v1/health` - 健康檢查
- 回傳服務健康狀態。

### 5. `GET /api/v1/status` - 狀態查詢
- 回傳系統運行狀態與版本資訊。

---

## 請求/回應格式

### 1. `POST /api/v1/query`

**Request**
```json
{
  "query": "請描述 2023/12/01 18:00-18:10 入口監控畫面有無異常？",
  "video_id": "entrance_20231201",
  "top_k": 5
}
```

**Response**
```json
{
  "answer": "2023/12/01 18:00-18:10 入口監控畫面未發現異常事件。",
  "retrieval_results": [
    {
      "segment_id": "entrance_20231201_001",
      "score": 0.92,
      "summary": "正常進出，無異常。"
    }
  ],
  "llm_model": "gpt-4o-mini",
  "timestamp": "2025-12-18T03:00:00Z"
}
```

**JSON Schema**
```json
{
  "type": "object",
  "properties": {
    "query": {"type": "string"},
    "video_id": {"type": "string"},
    "top_k": {"type": "integer"}
  },
  "required": ["query", "video_id"]
}
```

---

### 2. `POST /api/v1/retrieval/search`

**Request**
```json
{
  "query": "有無異常事件？",
  "video_id": "entrance_20231201",
  "top_k": 3
}
```

**Response**
```json
{
  "results": [
    {
      "segment_id": "entrance_20231201_001",
      "score": 0.92,
      "summary": "正常進出，無異常。"
    }
  ]
}
```

---

### 3. `POST /api/v1/llm/generate`

**Request**
```json
{
  "prompt": "根據以下檢索結果，請生成簡要說明：...",
  "model": "gpt-4o-mini"
}
```

**Response**
```json
{
  "answer": "根據檢索結果，未發現異常事件。"
}
```

---

### 4. `GET /api/v1/health`

**Response**
```json
{
  "status": "ok",
  "timestamp": "2025-12-18T03:00:00Z"
}
```

---

### 5. `GET /api/v1/status`

**Response**
```json
{
  "status": "running",
  "version": "v1.0.0",
  "llm_model": "gpt-4o-mini",
  "retrieval_backend": "VLM-RAG"
}
```

---

## 錯誤處理

### 錯誤碼列表

| 狀態碼 | 說明           |
|--------|----------------|
| 400    | 請求參數錯誤   |
| 404    | 資源不存在     |
| 500    | 伺服器內部錯誤 |

### 錯誤訊息格式

```json
{
  "error": {
    "code": 400,
    "message": "Missing required field: query"
  }
}
```

### 錯誤處理範例

- 請求缺少必要欄位時回傳 400
- 查無資料時回傳 404
- 未預期錯誤回傳 500

---

## 使用範例

### curl 範例

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "請描述 2023/12/01 18:00-18:10 入口監控畫面有無異常？", "video_id": "entrance_20231201"}'
```

### Python requests 範例

```python
import requests

url = "http://localhost:8000/api/v1/query"
payload = {
    "query": "請描述 2023/12/01 18:00-18:10 入口監控畫面有無異常？",
    "video_id": "entrance_20231201"
}
resp = requests.post(url, json=payload)
print(resp.json())

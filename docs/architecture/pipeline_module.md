# Pipeline Module 設計

## 模組職責

Pipeline Module 負責協調檢索（Retrieval）與生成（LLM）模組，實現查詢處理的完整流程。負責狀態管理、錯誤處理、降級策略，並作為 API 與核心模組的橋樑。

---

## 類別設計

### VQAPipeline 類別

```python
class VQAPipeline:
    def __init__(self, retrieval_client, llm_client):
        ...

    def process_query(self, query: str, video_id: str, top_k: int = 5) -> dict:
        """
        處理完整 VQA 查詢流程：
        1. 呼叫檢索模組取得相關片段
        2. 組合 prompt
        3. 呼叫 LLM 生成答案
        4. 回傳最終結果
        """
        ...
```

---

## 流程圖

```mermaid
flowchart TD
    A[接收查詢請求] --> B[檢索模組 search()]
    B --> C[組合 prompt]
    C --> D[LLM 生成答案]
    D --> E[組合回應]
    E --> F[回傳 API 結果]
    B -. 檢索失敗 .-> G[錯誤處理/降級]
    D -. 生成失敗 .-> G
```

---

## 狀態管理

- 管理每次查詢的唯一 ID、狀態（進行中、成功、失敗）
- 支援請求追蹤與日誌記錄

---

## 錯誤處理與降級策略

- 檢索或生成失敗時，回傳標準錯誤格式
- 支援部分結果回傳與預設答案
- 所有異常皆記錄日誌，便於追蹤

---

## 使用範例

```python
pipeline = VQAPipeline(retrieval_client, llm_client)
result = pipeline.process_query(query="有無異常？", video_id="entrance_20231201", top_k=3)
print(result["answer"])
```

---

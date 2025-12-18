# VLM-RAG 整合方案

## 1. RetrievalClient 介面設計

- `__init__(endpoint: str, api_key: str)`
- `search(query: str, video_id: str, top_k: int = 5) -> List[RetrievalResult]`
- `parse_results(raw_response: dict) -> List[RetrievalResult]`
- 支援異常處理（連線失敗、格式錯誤、超時等）

## 2. 與 Pipeline / LLM 的資料流

- Pipeline 呼叫 RetrievalClient.search()，取得檢索結果
- 檢索結果傳遞給 LLM Module 組合 prompt
- Pipeline 統一管理查詢狀態、錯誤與降級策略

## 3. 錯誤處理策略

- 檢索服務異常時，回傳預設錯誤訊息與空結果
- 支援重試與降級（如回傳部分結果）
- 所有異常皆記錄日誌

## 4. 預設參數建議

- top_k: 5
- timeout: 10 秒
- 支援 API 金鑰驗證

## 5. 資料格式

- 輸入：`{"query": str, "video_id": str, "top_k": int}`
- 輸出：`List[RetrievalResult]`，每筆包含 segment_id, score, summary

## 6. 測試與驗證

- 測試程式：`tests/integration/test_vlm_rag.py`
- 測試查詢集：`tests/data/rag_test_queries.json`
- 評估指標：Latency、Precision@K、Recall@K、F1@K

---

## 結論

本整合方案可確保 RetrievalClient 與 Pipeline/LLM 高效協作，並具備良好錯誤處理與擴展性。建議依據本方案實作與驗證。

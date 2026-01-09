# Phase 4 – UI 執行環境與基礎設施規劃（@INFRA）

## 1. UI 執行環境規劃摘要
- 目標：提供安防/管理人員可用的 Web/CLI 查詢介面，支援事件查詢、AI 回答、回饋。
- 建議技術：Streamlit（Web UI，快速原型）、FastAPI（API 串接）、Python CLI（備用）。
- 執行環境需求：
  - Python 3.8+
  - 已安裝 Streamlit、requests、相關 VQA Pipeline 依賴
  - .env 配置完整（API Key、服務端點等）

## 2. UI 相關目錄與結構說明
- `frontend/`
  - `app.py`（Web UI 主程式）
  - `components/`（可拆分 UI 元件）
  - `static/`（靜態資源）
  - `templates/`（如需自訂 HTML）
- `tests/integration/test_ui.py`（UI smoke test）

## 3. 必要配置項目清單
- `.env` 需包含：
  - VQA API 端點（如 VQA_API_URL）
  - LLM 相關金鑰
  - 預設查詢參數
- requirements.txt 需有：
  - streamlit
  - requests
  - fastapi（如需 API 層）

## 4. Smoke Test 流程描述
1. 啟動 Web UI：`streamlit run frontend/app.py`
2. 輸入查詢，送出
3. 檢查事件列表、AI 回答是否顯示
4. 點選/輸入回饋（滿意/不滿意）
5. 檢查回饋是否被記錄（log 或 DB）
6. 若任一步驟失敗，記錄錯誤並回報

---

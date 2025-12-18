# 開發指南（Development Guide）

## 專案概述

Visual_Question_Answering(VQA) 是一套結合 VLM-RAG 與 LLM 的安防視頻問答系統，支援用戶以自然語言查詢監控影片內容，並獲得智慧化答案。專案採用模組化設計，易於擴展與維護。

---

## 架構說明（簡化版）

- **Backend**: FastAPI + Python 3.10+
- **Frontend**: Streamlit（MVP）、React（長期）
- **Retrieval**: VLM-RAG
- **LLM**: OpenAI GPT-4o-mini
- **Deployment**: Docker, Docker Compose

---

## 開發規範

### 代碼風格

- 使用 [Black](https://black.readthedocs.io/en/stable/) 格式化
- 靜態檢查：Flake8、mypy
- 變數/類別/函式命名遵循 PEP8
- 註解與 docstring 採用 Google Style

### Git 提交規範

- 使用英文動詞開頭（feat, fix, refactor, docs, test, chore）
- 提交訊息簡明扼要，必要時補充說明

---

## 各 Agent 指南

### RAG Agent（檢索模組開發）

- 參考 `docs/architecture/retrieval_module.md`
- 負責與 VLM-RAG API 對接、資料結構設計、錯誤處理

### LLM Agent（生成模組開發）

- 參考 `docs/architecture/llm_module.md`
- 封裝 OpenAI API，設計 PromptManager，處理回應格式

### UI Agent（前端開發）

- MVP 階段以 Streamlit 為主，快速驗證用戶流程
- 長期可升級至 React + Ant Design

### QA Agent（測試策略）

- 撰寫單元測試（tests/unit/）、整合測試（tests/integration/）
- 覆蓋 API、Pipeline、Retrieval、LLM 各模組
- 使用 pytest、coverage 工具

---

## 常見問題（FAQ）

**Q: 如何本地啟動所有服務？**  
A: 使用 `docker-compose up` 一鍵啟動。

**Q: 如何新增 API 端點？**  
A: 於 `src/api/` 新增路由，並補充 Pydantic Model 與測試。

**Q: 如何調整檢索/生成參數？**  
A: 修改 `src/retrieval/config.py` 或 `src/llm/config.py`。

**Q: 如何驗證架構設計？**  
A: 參考 `docs/architecture/` 內所有文檔，並執行測試。

---

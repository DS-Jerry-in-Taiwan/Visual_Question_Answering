# Visual_Question_Answering(VQA) - 安防視頻問答系統

## 專案簡介
Visual_Question_Answering(VQA) 是一套結合多智能體（Multi-Agent）協作的安防視頻問答系統，旨在讓使用者能以自然語言查詢監控影片內容，並獲得智慧化、即時的答案。系統整合 VLM-RAG（視覺語言檢索生成）與 LLM（大型語言模型），提供高效檢索、語意理解與答案生成能力。

本專案採用現代化技術棧，支援多階段開發流程，適合企業級安防應用、智慧城市、事件追蹤等場景。團隊以模組化、可擴展為核心設計原則，確保後續維護與功能擴充的便利性。

## Multi-Agent 開發團隊

| Agent 名稱 | 角色             | 職責描述                                      |
|------------|------------------|-----------------------------------------------|
| PM         | Project Manager  | 專案初始化、進度管理、協作協調                |
| ARCH       | System Architect | 系統架構設計、API 規劃、技術棧決策            |
| RAG        | Retrieval Expert | VLM-RAG 檢索優化、嵌入調校、檢索 API 實作      |
| LLM        | LLM Expert       | LLM 整合、提示詞設計、生成優化                |
| UI         | Frontend Engineer| 前端開發、API 整合、介面設計                  |
| QA         | Quality Assurance| 測試設計、品質分析、評估與回饋                |

## 核心功能
- 自然語言查詢
- 智慧檢索（VLM-RAG）
- 答案生成（LLM）
- 視覺化介面（Streamlit/React）

## 技術棧

### 後端
- Python 3.10+
- FastAPI
- VLM-RAG（既有系統）
- OpenAI API / Claude API

### 前端
- Streamlit（MVP）
- React + Ant Design（長期）

### 部署
- Docker
- Docker Compose

## 開發階段

- Phase 0: 專案初始化（Day 1-2）
- Phase 1: RAG 模組優化（Day 3-5）
- Phase 2: LLM 整合（Day 6-8）
- Phase 3: Pipeline 整合（Day 9-10）
- Phase 4: 前端開發（Day 11-14）
- Phase 5: 測試與評估（Day 15-17）

## 快速開始

### 環境需求
- Python 3.10 以上
- pip
- Docker（建議）
- 建議使用虛擬環境（venv）

### 安裝步驟

```bash
# 1. 下載專案
git clone https://github.com/your-org/Visual_Question_Answering-VQA.git
cd Visual_Question_Answering\(VQA\)

# 2. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 複製環境變數範本
cp .env.example .env

# 5. 啟動後端服務
uvicorn src.api.vqa_api:app --reload

# 6. 啟動前端（Streamlit）
streamlit run frontend/app.py
```

## 專案結構

```
Visual_Question_Answering(VQA)/
├── configs/
├── docker/
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── guides/
│   ├── llm/
│   ├── optimization/
│   └── retrieval/
├── frontend/
│   └── app.py
├── scripts/
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   ├── llm/
│   │   ├── __init__.py
│   ├── pipeline/
│   │   ├── __init__.py
│   ├── retrieval/
│   │   ├── __init__.py
│   └── utils/
│       ├── __init__.py
└── tests/
    ├── __init__.py
    ├── data/
    ├── integration/
    │   ├── __init__.py
    ├── reports/
    └── unit/
        ├── __init__.py
```

## 開發規範

- 詳細請參見 [docs/guides/](docs/guides/)

## 授權

MIT License

## 聯絡資訊

- 專案負責人：PM Agent
- Email: pm@your-org.com

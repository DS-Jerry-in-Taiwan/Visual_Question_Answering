# ADR-005: 使用 Docker 部署

## 狀態
已採用

## 背景
本專案包含多個後端模組（API、Pipeline、Retrieval、LLM）、前端服務與外部依賴（VLM-RAG、OpenAI API）。需確保部署一致性、易於測試與擴展，並支援本地與雲端多環境。

## 決策
選擇 [Docker](https://www.docker.com/) 進行容器化部署，並以 Docker Compose 編排多服務。

## 理由
- 環境一致性高，減少「在我機器上沒問題」情境
- 易於本地開發、測試與 CI/CD 整合
- 支援多服務協同（API、前端、測試等）
- 可彈性擴展、升級與回滾
- 社群活躍，文件完整

## 後果
- 部署流程自動化，維運成本降低
- 可快速複製與擴展環境
- 需學習 Docker 與 Compose 基本操作

## 替代方案
- 傳統裸機/虛擬機部署：彈性高但維護成本大
- Kubernetes：適合大規模雲端，但初期複雜度高
- Heroku/Serverless：適合小型專案但彈性較低

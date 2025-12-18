# ADR-001: 使用 FastAPI

## 狀態
已採用

## 背景
本專案需提供高效、易擴展的 RESTful API，並支援自動文件產生、型別驗證與現代 Python 生態整合。傳統 Flask 雖簡單，但型別驗證與 OpenAPI 支援較弱。

## 決策
選擇 [FastAPI](https://fastapi.tiangolo.com/) 作為後端 API 框架。

## 理由
- 型別安全，支援 Pydantic 資料驗證
- 自動產生 OpenAPI/Swagger 文件
- 非同步支援佳，效能高
- 社群活躍，文件完整
- 易於與現代 Python 工具鏈整合

## 後果
- API 開發效率提升
- 測試與維護成本降低
- 可直接產生互動式 API 文件
- 需學習 FastAPI 特有語法

## 替代方案
- Flask：生態成熟但型別驗證弱
- Django REST Framework：功能強大但較重
- Starlette：輕量但需自行組裝

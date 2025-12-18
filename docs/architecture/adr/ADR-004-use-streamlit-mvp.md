# ADR-004: 使用 Streamlit（MVP）

## 狀態
已採用

## 背景
本專案需快速驗證 VQA 系統的用戶體驗與端到端流程。Streamlit 提供極速開發、互動式 Web UI，適合 MVP 階段展示與測試。

## 決策
選擇 [Streamlit](https://streamlit.io/) 作為 MVP 階段的前端框架。

## 理由
- 開發速度快，無需前端專業知識
- 支援 Python 直寫互動式 UI
- 易於與 FastAPI、後端模組整合
- 社群活躍，文件完整
- 適合內部驗證與快速迭代

## 後果
- 可快速產出可用原型，驗證用戶流程
- 不適合長期複雜前端需求
- 後續可平滑升級至 React 等框架

## 替代方案
- React + Ant Design：適合長期發展但開發週期長
- Gradio：適合 AI Demo，但自訂性較低
- Flask + Jinja2：需自行處理前端模板，開發效率較低

# ADR-002: 使用 OpenAI GPT-4o-mini

## 狀態
已採用

## 背景
本專案需具備強大的自然語言理解與生成能力，並能靈活處理多語言、複雜查詢。OpenAI GPT-4o-mini 提供高品質生成、低延遲與穩定 API，適合安防 VQA 應用。

## 決策
選擇 [OpenAI GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o) 作為主要 LLM 生成模型。

## 理由
- 支援多語言與複雜語意理解
- 生成品質高，回應自然
- API 易於整合，生態成熟
- 支援 prompt 工程與多模型切換
- 成本效益佳，延遲低

## 後果
- 可快速實現高品質問答生成
- 依賴外部雲端服務，需管理 API 金鑰與流量
- 需考慮資安與隱私議題

## 替代方案
- GPT-3.5/4：品質佳但成本較高
- Llama 3、Gemini：開源或其他雲端 LLM，需額外部署或評估
- 自建 LLM：彈性高但維護成本大

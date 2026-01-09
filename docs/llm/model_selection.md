# LLM 模型選擇與準備指引（Phase 2 - INFRA）

## 候選模型比較

| 模型                | Token 價格（USD/1K） | 上下文長度 | API 穩定性 | 適用場景         |
|---------------------|---------------------|------------|------------|------------------|
| GPT-4o-mini         | $0.005 / $0.015     | 128K       | 穩定       | 泛用、低成本     |
| GPT-4               | $0.03 / $0.06       | 128K       | 穩定       | 高準確需求       |
| Claude 3.5 Sonnet   | $0.003 / $0.015     | 200K       | 穩定       |長上下文、泛用    |

- 價格為 Input/Output token
- 皆支援高上下文長度，API 穩定
- Claude 3.5 Sonnet 價格最低，GPT-4o-mini 性價比高

## 推薦建議

- **推薦模型：GPT-4o-mini**
  - 價格低、上下文長度充足、API 穩定
  - 適合大多數 VQA 任務
  - 若需更長上下文可考慮 Claude 3.5 Sonnet

## 模型準備與 API 設定步驟

1. 註冊 OpenAI 或 Anthropic 帳號，取得 API Key。
2. 於 `.env` 或 `configs/default.yaml` 設定下列欄位：
   - `llm_provider`: openai 或 anthropic
   - `llm_model`: gpt-4o, gpt-4, claude-3.5-sonnet 等
   - `llm_api_base`: API 端點（如 https://api.openai.com/v1）
   - `llm_api_key`: 你的 API Key
3. 若使用本地模型，請參考 docs/llm/model_selection.md 相關章節（可擴充）。
4. 依需求調整 `embedding_model` 欄位（如 BAAI/bge-m3）。

## 參考依據

- OpenAI 官方文件
- Anthropic 官方文件
- Phase 2 context 文檔

# LLM Module 設計

## 模組職責

LLM Module 封裝與 OpenAI GPT-4o-mini API 的互動，負責根據檢索結果與用戶查詢生成自然語言答案。支援 Prompt 管理、模型選擇與錯誤處理，為 Pipeline Module 提供高品質生成服務。

---

## 類別設計

### LLMClient 類別

```python
class LLMClient:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        ...

    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 1000) -> "LLMResponse":
        """呼叫 LLM API 生成答案"""
        ...
```

### PromptManager 類別

```python
class PromptManager:
    def __init__(self, templates: dict):
        ...

    def build_prompt(self, query: str, retrieval_results: list) -> str:
        """根據查詢與檢索結果組合 prompt"""
        ...
```

---

## 資料模型

### LLMRequest

```python
class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 1000
```

### LLMResponse

```python
class LLMResponse(BaseModel):
    answer: str
    model: str
    usage: dict = None
```

---

## Prompt 模板設計

- 支援多種查詢場景（異常摘要、事件描述、影片摘要等）
- 可根據 retrieval_results 動態插入內容
- 範例模板：

```jinja2
請根據以下檢索結果，簡要回答用戶問題：
用戶問題：{{ query }}
檢索摘要：
{% for r in retrieval_results %}
- {{ r.summary }} (分數: {{ r.score }})
{% endfor %}
請以簡潔中文回答。
```

---

## 錯誤處理策略

- LLM API 連線失敗、超時時，回傳預設錯誤訊息
- 回傳格式異常時，記錄日誌並回傳標準錯誤格式
- 支援重試與降級策略（如回傳部分答案）

---

## 使用範例

```python
llm = LLMClient(api_key="your_openai_key")
prompt_mgr = PromptManager(templates={"default": "請根據以下檢索結果...{{ query }}..."})
prompt = prompt_mgr.build_prompt(query="有無異常？", retrieval_results=[...])
resp = llm.generate(prompt)
print(resp.answer)
```

---

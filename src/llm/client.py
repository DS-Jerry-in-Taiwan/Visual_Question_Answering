from src.llm.config import LLMConfig
from typing import Any, Dict
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

class LLMClient:
    """
    LLMClient: Handles interaction with LLM provider (e.g., OpenAI).
    """

    def __init__(self, config: LLMConfig):
        self.config = config

    async def generate(self, prompt: str, context: list = None) -> Dict[str, Any]:
        """
       
        """
        if context:
            context_text = "\n".join(
                [f"{item['description']} (score: {item['score']})" for item in context]
            )
            full_prompt = (
                "請根據下列事件紀錄，先列出所有異常事件摘要（每行一筆，格式：時間＋描述＋score），"
                "再根據這些事件回答用戶的問題。\n\n"
                f"事件紀錄：\n{context_text}\n\n問題：\n{prompt}"
            )
        else:
            full_prompt = prompt

        if ChatOpenAI is None:
            raise ImportError("請安裝 langchain_openai 套件，或改用 openai 官方 SDK。")
        llm = ChatOpenAI(
            openai_api_key=self.config.api_key,
            model_name=self.config.model,
            temperature=0.2,
        )
        # 構造 langchain chat message 格式
        from langchain_core.messages import HumanMessage
        messages = [[HumanMessage(content=full_prompt)]]
        response = await llm.agenerate(messages)
        answer = response.generations[0][0].text
        return {
            "answer": answer,
            "model": self.config.model,
            "provider": self.config.provider
        }

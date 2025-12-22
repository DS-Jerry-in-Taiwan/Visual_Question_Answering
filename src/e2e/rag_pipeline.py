from src.pipeline.query_pipeline import QueryPipeline
from src.llm.client import LLMClient
from typing import Any, Dict

class E2ERAGPipeline:
    """
    E2ERAGPipeline: End-to-end pipeline integrating retrieval and LLM.
    """

    def __init__(self, query_pipeline: QueryPipeline, llm_client: LLMClient):
        self.query_pipeline = query_pipeline
        self.llm_client = llm_client

    async def query(self, user_query: str) -> Dict[str, Any]:
        """
        Run end-to-end retrieval and LLM generation.
        """
        retrieval_result = await self.query_pipeline.process(user_query)
        context = retrieval_result.get("formatted_context", "")
        llm_response = await self.llm_client.generate(context)
        return {
            "answer": llm_response["answer"],
            "context": context,
            "retrieval_results": retrieval_result.get("results", []),
            "metadata": retrieval_result.get("metadata", {})
        }

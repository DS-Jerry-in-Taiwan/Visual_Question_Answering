from src.pipeline.config import PipelineConfig
from typing import Any, Dict

class QueryPipeline:
    """
    QueryPipeline: Orchestrates query processing and retrieval.
    """

    def __init__(self, retrieval_client: Any, config: PipelineConfig):
        self.retrieval_client = retrieval_client
        self.config = config

    async def process(self, query: str) -> Dict[str, Any]:
        """
        Process a query through the pipeline and return formatted results.
        """
        results = await self.retrieval_client.search(query)
        return {
            "formatted_context": f"Context for: {query}",
            "results": results,
            "metadata": {"top_k": self.config.default_top_k}
        }

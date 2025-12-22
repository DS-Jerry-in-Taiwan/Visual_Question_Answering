import json
import asyncio
from src.e2e.rag_pipeline import E2ERAGPipeline
from src.pipeline.query_pipeline import QueryPipeline
from src.llm.client import LLMClient
from src.llm.config import LLMConfig

def load_queries(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

async def main():
    # Replace with actual pipeline and client initialization as needed
    mock_query_pipeline = QueryPipeline(None, None)  # Replace with real instance
    llm_config = LLMConfig(api_key="test_key")
    llm_client = LLMClient(llm_config)
    pipeline = E2ERAGPipeline(mock_query_pipeline, llm_client)

    queries = load_queries("tests/data/e2e_eval_queries.json")
    results = []
    for q in queries:
        result = await pipeline.query(q["query"])
        results.append({
            "query": q["query"],
            "context": result.get("context"),
            "answer": result.get("answer"),
            "retrieval_results": result.get("retrieval_results"),
            "metadata": result.get("metadata")
        })

    with open("tests/reports/step14_e2e_eval_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())

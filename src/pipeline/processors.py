from typing import Any, Dict, List

class QueryProcessor:
    """
    QueryProcessor: Cleans and prepares queries for retrieval.
    """
    def clean_query(self, query: str) -> str:
        # Example: basic whitespace normalization
        return query.strip()

    def deduplicate(self, queries: List[str]) -> List[str]:
        # Remove duplicate queries
        return list(dict.fromkeys(queries))

class ResultProcessor:
    """
    ResultProcessor: Processes and filters retrieval results.
    """
    def filter_results(self, results: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
        # Filter results by score threshold
        return [r for r in results if r.get("score", 0) >= threshold]

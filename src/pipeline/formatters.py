from typing import Any, Dict, List


class ContextFormatter:
    """
    ContextFormatter: Formats context for LLM or output.
    """

    def format_for_llm(self, query: str, results: List[Dict[str, Any]]) -> str:
        # Example: format context for LLM prompt
        context_lines = [f"Query: {query}"]
        for r in results:
            context_lines.append(f"- [{r.get('score', 0):.2f}] {r.get('content', '')}")
        return "\n".join(context_lines)

    def format_compact(self, results: List[Dict[str, Any]]) -> str:
        # Compact format for UI or logs
        return "; ".join([r.get("content", "") for r in results])

    def format_detailed(self, results: List[Dict[str, Any]]) -> str:
        # Detailed format for debugging or analysis
        return "\n".join(
            [
                f"ID: {r.get('id', '')}, Score: {r.get('score', 0)}, Content: {r.get('content', '')}"
                for r in results
            ]
        )

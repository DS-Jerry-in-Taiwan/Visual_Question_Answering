from src.pipeline.formatters import ContextFormatter

def test_format_for_llm():
    formatter = ContextFormatter()
    query = "Test Query"
    results = [
        {"score": 0.9, "content": "A"},
        {"score": 0.5, "content": "B"},
    ]
    output = formatter.format_for_llm(query, results)
    assert "Query: Test Query" in output
    assert "- [0.90] A" in output
    assert "- [0.50] B" in output

def test_format_compact():
    formatter = ContextFormatter()
    results = [
        {"content": "A"},
        {"content": "B"},
    ]
    output = formatter.format_compact(results)
    assert output == "A; B"

def test_format_detailed():
    formatter = ContextFormatter()
    results = [
        {"id": "1", "score": 0.9, "content": "A"},
        {"id": "2", "score": 0.5, "content": "B"},
    ]
    output = formatter.format_detailed(results)
    assert "ID: 1, Score: 0.9, Content: A" in output
    assert "ID: 2, Score: 0.5, Content: B" in output

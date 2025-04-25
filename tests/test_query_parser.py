
import pytest
from agent.query_parser import QueryParser

def test_query_parser_keywords_extraction():
    parser = QueryParser()
    query = "Impact of AI on healthcare in 2025"
    parsed = parser.parse(query)
    assert "keywords" in parsed
    assert isinstance(parsed["keywords"], list)
    assert "AI" in parsed["keywords"] or "healthcare" in parsed["keywords"]

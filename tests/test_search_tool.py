 
import pytest
from agent.search_tool import WebSearchTool

def test_search_returns_results():
    searcher = WebSearchTool()
    results = searcher.search("latest AI trends")
    assert isinstance(results, list)
    assert all('title' in result and 'link' in result for result in results)

 
import pytest
from agent.analyzer import ContentAnalyzer

def test_content_analyzer_generate_summary():
    analyzer = ContentAnalyzer(model="gemini-1.5-flash")  # whichever you prefer
    prompt = "Summarize the importance of AI in education."
    response = analyzer.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 10

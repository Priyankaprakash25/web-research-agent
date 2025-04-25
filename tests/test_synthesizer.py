 
import pytest
from agent.synthesizer import SummarySynthesizer

def test_synthesizer_combines_summaries():
    synthesizer = SummarySynthesizer(model="gemini-1.5-flash")
    summaries = ["AI is transforming healthcare.", "AI is also transforming education."]
    query = "How AI is changing different industries?"
    final_report = synthesizer.combine_summaries(summaries, query)
    assert isinstance(final_report, str)
    assert "AI" in final_report

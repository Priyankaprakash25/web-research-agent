 
import pytest
from agent.scraper import WebScraper

def test_scrape_returns_content():
    scraper = WebScraper()
    # Use a simple publicly available page
    content = scraper.scrape("https://example.com")
    assert isinstance(content, str)
    assert len(content) > 0

# agent/scraper.py

import requests
from bs4 import BeautifulSoup
from typing import Optional

class WebScraper:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def scrape(self, url: str) -> Optional[str]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Heuristic: get largest text block in <p> tags
            paragraphs = soup.find_all("p")
            text = "\n".join(p.get_text() for p in paragraphs if len(p.get_text()) > 50)

            return text.strip() if text else None

        except Exception as e:
            print(f"[ERROR] Could not scrape {url}: {e}")
            return None

# Test mode
if __name__ == "__main__":
    scraper = WebScraper()
    url = "https://edtechmagazine.com/k12/article/2024/09/ai-education-2024-educators-express-mixed-feelings-technologys-future-perfcon"
    content = scraper.scrape(url)

    if content:
        print("✅ Extracted content (first 1000 chars):\n")
        print(content[:1000])
    else:
        print("❌ Failed to extract content.")

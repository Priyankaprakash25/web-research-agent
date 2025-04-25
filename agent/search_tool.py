import os
import requests
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

class WebSearchTool:
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.api_url = "https://google.serper.dev/search"

    def search(self, query: str) -> List[Dict]:
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 5  # number of search results
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("organic", [])  # list of {title, link, snippet}
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []

if __name__ == "__main__":
    tool = WebSearchTool()
    results = tool.search("Latest trends in AI for education 2024")
    
    for result in results:
        print(f"Title: {result.get('title')}")
        print(f"Link: {result.get('link')}")
        print(f"Snippet: {result.get('snippet')}")
        print("-" * 40)

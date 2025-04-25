import re
from typing import List, Dict

class QueryParser:
    def __init__(self):
        self.query_type_keywords = {
            "news": ["latest", "breaking", "news", "trending"],
            "factual": ["what is", "define", "explain", "who is", "history of"],
            "how-to": ["how to", "steps to", "guide", "tutorial"]
        }

    def classify_query(self, query: str) -> str:
        query = query.lower()
        for qtype, keywords in self.query_type_keywords.items():
            if any(kw in query for kw in keywords):
                return qtype
        return "general"

    def extract_keywords(self, query: str) -> List[str]:
        # Remove stop words and symbols (very basic version)
        stop_words = {"the", "is", "a", "of", "and", "to", "in", "on", "for", "with", "at"}
        words = re.findall(r'\w+', query.lower())
        return [w for w in words if w not in stop_words]

    def parse(self, query: str) -> Dict:
        return {
            "original_query": query,
            "query_type": self.classify_query(query),
            "keywords": self.extract_keywords(query)
        }

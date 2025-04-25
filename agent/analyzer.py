import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

from agent.config import configure_gemini  # ← import the utility

class ContentAnalyzer:
    def __init__(self, model="gemini-1.5-pro"):
        self.model_name = model
        self.model = configure_gemini(model)  # ✅ use selected model

    def summarize(self, content: str, query: str) -> str:
        try:
            prompt = (
                f"You are a research assistant. A user asked:\n'{query}'\n\n"
                f"Here is an article/content:\n\n{content[:3000]}\n\n"
                f"Give a short, factual summary based only on the content above. "
                f"If the content is irrelevant, say: 'No useful information found in this source.'"
            )
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini summarization failed: {e}")
            return "Summary unavailable due to an error."

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] Gemini generation failed: {e}")
            return "Follow-up unavailable due to an error."

# Optional test block
if __name__ == "__main__":
    from scraper import WebScraper

    scraper = WebScraper()
    url = "https://edtechmagazine.com/k12/article/2024/09/ai-education-2024-educators-express-mixed-feelings-technologys-future-perfcon"
    content = scraper.scrape(url)

    if content:
        analyzer = ContentAnalyzer()
        summary = analyzer.summarize(content, "Impact of AI in education in 2024")
        print("🧠 Gemini Summary:\n", summary)
    else:
        print("❌ Failed to extract content.")

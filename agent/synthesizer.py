from typing import List
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

from agent.config import configure_gemini

class SummarySynthesizer:
    def __init__(self, model="gemini-1.5-pro"):
        self.model = configure_gemini(model)  # ✅ use passed model

    def combine_summaries(self, summaries: List[str], query: str) -> str:
        try:
            summaries_text = "\n\n".join(
                [f"Source {i+1}:\n{summary}" for i, summary in enumerate(summaries)]
            )
            prompt = (
                f"A user asked:\n'{query}'\n\n"
                f"Here are multiple AI-generated summaries based on different sources:\n\n"
                f"{summaries_text}\n\n"
                f"Your job is to create a final research summary for the user. It should:\n"
                f"- Be well-structured\n"
                f"- Avoid repeating the same points\n"
                f"- Present different angles if any\n"
                f"- Be no more than 250 words\n"
            )

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"[ERROR] Synthesizing failed: {e}")
            raise e  # 🔥 KEY FIX: re-raise to be caught in app.py

# Test block
if __name__ == "__main__":
    fake_summaries = [
        "AI in education can help personalize learning and automate admin work.",
        "Educators are optimistic about AI, but adoption is slow due to lack of training.",
        "Most teachers see potential in generative AI, but few are confident using it."
    ]

    query = "Impact of AI in education in 2024"
    synthesizer = SummarySynthesizer()
    final_summary = synthesizer.combine_summaries(fake_summaries, query)
    print("📋 Final Research Summary:\n", final_summary)

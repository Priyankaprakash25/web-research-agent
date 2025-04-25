# agent/config.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def configure_gemini(model_name: str):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel(model_name)

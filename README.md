# Web Research Agent 🚀

🤖 An AI-powered Web Research Agent built using **Streamlit** + **Google Gemini APIs**.  
It intelligently analyzes user queries, performs real-time web searches, extracts data from multiple sources, and generates clean, concise research summaries — all with minimal human input.

---

## 📌 Features

- ✨ Understands complex user queries and breaks them into searchable components
- 🔎 Performs real-time web searches using simulated Serper API
- 🖥️ Scrapes and extracts relevant data using BeautifulSoup
- 🧠 Analyzes and synthesizes multi-source information into a single cohesive summary
- 🔁 **Bonus:** Smartly detects and handles follow-up queries vs new topics (optional enhancement)
- 📥 One-click download of generated research summaries
- 🛡️ Robust error handling: quota, search failure, scraping issues, etc.
- 🎛️ Model switching: Easily toggle between **Gemini-1.5-Pro** and **Gemini-1.5-Flash**
- ✅ Fully unit tested using **Pytest**

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    A[User Query] --> B[Query Parser]
    B --> C[Web Search Tool]
    C --> D[Web Scraper]
    D --> E[Content Analyzer]
    E --> F[Summary Synthesizer]
    F --> G[Streamlit UI Response]
    G --> H[Download Button]
    G --> I[Follow-Up Detection]

---

## 🛠️ Tools Used

| Component | Tool | Description |
|:----------|:-----|:------------|
| AI Model | Google Gemini 1.5 Pro / Flash | For summarizing and synthesizing |
| Search | WebSearchTool (Serper API simulated) | Perform Google-like searches |
| Scraping | WebScraper (BeautifulSoup) | Extract text from websites |
| Content Analysis | ContentAnalyzer | Summarize scraped content |
| Query Analysis | QueryParser | Break down queries into search keywords |
| Framework | Streamlit | Frontend UI |
| Testing | Pytest | Unit testing core modules |

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/web-research-agent.git
cd web-research-agent
```

2. **Install requirements:**

```bash
pip install -r requirements.txt
```

3. **Set up `.env`:**

```plaintext
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```

4. **Run the app:**

```bash
streamlit run app.py
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

✅ 5/5 Tests Passing.

---

## 🛡️ Error Handling

| Situation | Handling |
|:----------|:---------|
| No search results | Show user-friendly error |
| Scraping failures | Skip that source |
| Gemini API quota limits | Alert user to switch model |
| Unexpected system error | Logged in `app.log` and user informed |

---

## 📷 GDrive Video 
🔗[Link](https://drive.google.com/file/d/1sPscbmhHlYJV3JejPAbYUFvtQFf3_Ya9/view?usp=sharing)


---

## 👨‍💻 Built By

**Priyanka N J**  
🔗 [Email Me](mailto:priyanwork2@gmail.com)

---


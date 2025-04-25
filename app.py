import streamlit as st
from agent.query_parser import QueryParser
from agent.search_tool import WebSearchTool
from agent.scraper import WebScraper
from agent.analyzer import ContentAnalyzer
from agent.synthesizer import SummarySynthesizer
import logging
import os
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from difflib import SequenceMatcher
import re

# Load environment
load_dotenv()
def configure_gemini(model: str):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel(model)

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Page config
st.set_page_config(page_title="🔍 AI Research Agent", layout="wide")

# ---- CSS Styling ----
st.markdown("""
    <style>
        body { background-color: #0e1117; }
        .title { font-size: 36px; color: #2F80ED; font-weight: 700; }
        .subtitle { font-size: 20px; color: #ccc; margin-bottom: 30px; }
        .result-box {
            background-color: #1c1f26;
            border-left: 6px solid #2F80ED;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            color: #fff;
        }
        .footer { font-size: 13px; color: gray; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# ---- Session State Init ----
for k in ["chat_history", "last_query", "last_summary"]:
    if k not in st.session_state:
        st.session_state[k] = [] if k == "chat_history" else ""

# ---- Title + Input ----
st.markdown('<div class="title">🤖 Web Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask anything and get a clean, AI-generated research report from real-time web data.</div>', unsafe_allow_html=True)
query = st.text_input("", key="user_query", placeholder="Type your research question here...")

# ---- Follow-up Detection ----
def is_followup_query(new_query, last_query):
    if not last_query or not new_query.strip():
        return False

    new_q = new_query.strip().lower()
    last_q = last_query.strip().lower()

    if re.match(r"^(what|why|how|does|do|is|are|then|can|should|will)\b", new_q) and len(new_q.split()) <= 12:
        return True

    overlap = len(set(new_q.split()) & set(last_q.split()))
    if overlap / max(len(set(last_q.split())), 1) < 0.3:
        return False

    return False

is_followup = is_followup_query(query, st.session_state.last_query)


# ---- Sidebar ----
st.sidebar.markdown("### Model Settings")
selected_model = st.sidebar.selectbox("Choose Gemini Model:", options=["gemini-1.5-pro", "gemini-1.5-flash"])
logger.info(f"🔁 Using Gemini Model: {selected_model}")

# ---- Action Buttons ----
col1, col2 = st.columns([1, 1])
with col1:
    run_clicked = st.button("🚀 Run Agent", key="run_agent")
with col2:
    clear_clicked = st.button("🧹 Clear Chat History", key="clear_chat")

if clear_clicked:
    for k in ["chat_history", "last_query", "last_summary"]:
        st.session_state[k] = [] if k == "chat_history" else ""
    st.rerun()

# ---- Run Agent Logic ----
if run_clicked and query:
    with st.spinner("🤖 Crunching the internet... please hold tight..."):
        try:
            is_followup = is_followup_query(query, st.session_state.last_query)

            if is_followup:
                # Generate follow-up using context
                prompt = f"""Previous Query: {st.session_state.last_query}
Previous Summary:
{st.session_state.last_summary}

Follow-Up Question: {query}
Please respond using the original context + this follow-up."""
                analyzer = ContentAnalyzer(model=selected_model)
                response = analyzer.generate(prompt)

                st.session_state.chat_history.append({
                    "query": query,
                    "response": response,
                    "followup": True
                })

            else:
                # Fresh query: search, scrape, analyze, and summarize
                parser = QueryParser()
                parsed = parser.parse(query)
                keywords = " ".join(parsed["keywords"])

                searcher = WebSearchTool()
                results = searcher.search(keywords)

                if not results:
                    st.error("No search results found. Try a different query.")
                else:
                    scraper = WebScraper()
                    analyzer = ContentAnalyzer(model=selected_model)
                    summaries = []
                    for result in results[:3]:
                        st.markdown(f"🌐 **Scraping:** {result['title']}", unsafe_allow_html=True)
                        content = scraper.scrape(result["link"])
                        if content:
                            summary = analyzer.summarize(content, query)
                            summaries.append(summary)

                    if summaries:
                        synthesizer = SummarySynthesizer(model=selected_model)
                        final_report = synthesizer.combine_summaries(summaries, query)

                        st.session_state.chat_history.append({
                            "query": query,
                            "response": final_report,
                            "followup": False
                        })
                        st.session_state.last_query = query
                        st.session_state.last_summary = final_report

                    else:
                        st.warning("No usable summaries could be created.")
        except Exception as e:
            logger.error(f"[ERROR] {e}")
            err_msg = str(e).lower()
            if any(k in err_msg for k in ["quota", "rate limit", "429", "exceeded", "limit"]):
                st.error(f"⚠️ Quota exceeded for `{selected_model}`. Try switching model or wait.")
            else:
                st.error(f"⚠️ Something went wrong: {e}")

# ✅ Always show download for latest full summary (only if not follow-up)
if st.session_state.chat_history and not st.session_state.chat_history[-1]["followup"]:
    latest = st.session_state.chat_history[-1]
    st.download_button(
        "📥 Download Summary",
        data=latest["response"],
        file_name="research_summary.txt",
        key=f"download_{uuid.uuid4()}"
    )

# ---- Show Chat History ----
for chat in st.session_state.chat_history:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"### {'🧠 Follow-Up Response' if chat['followup'] else '📋 Final Research Summary'}")
    st.markdown(f"**You:** {chat['query']}")
    st.write(chat["response"])
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer ----
st.sidebar.image("https://blog.bismart.com/hs-fs/hubfs/Imported_Blog_Media/los-10-mejores-bots-disponibles-en-Internet-Sep-26-2023-08-53-22-8616-AM.jpg", width=80)
st.sidebar.markdown("### Masonry AI Agent")
st.sidebar.markdown("Built by [Priyanka N J](mailto:priyanwork2@gmail.com) using Streamlit + Gemini")
st.markdown('<div class="footer">Made with ✨ using OpenAI, Gemini, Serper, Streamlit & BeautifulSoup</div>', unsafe_allow_html=True)

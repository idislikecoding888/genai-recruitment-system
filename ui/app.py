import streamlit as st
import os
import sys
import time
import re

# Disable CrewAI telemetry immediately at startup to avoid thread/signal errors
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# Add parent directory to path to import main logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_recruitment_flow, save_to_vault, search_vault, get_all_vault_resumes, clear_vault
from tools.pdf_processor import extract_text_from_pdf

# --- Page Config ---
st.set_page_config(
    page_title="Smart Hire | Recruitment Intelligence",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #210635, #420D4B, #7B337E);
    color: #F5D5E0;
}

.main-header {
    background: linear-gradient(90deg, #F5D5E0, #6667AB, #7B337E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3.5rem;
}

.subtitle {
    color: #F5D5E0;
    font-size: 1.1rem;
    opacity: 0.85;
}

.glass-card {
    background: rgba(66, 13, 75, 0.55);
    border-radius: 16px;
    padding: 1.8rem;
    backdrop-filter: blur(16px);
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-header">Smart Hire</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Recruitment Intelligence Platform</p>', unsafe_allow_html=True)

# --- Metrics Extraction ---
match_score = "--"
hiring_difficulty = "Pending"

if "last_result" in st.session_state and st.session_state.last_result:

    report_text = str(st.session_state.last_result.raw)

    score_match = re.search(r"(\d+)/100", report_text)
    if score_match:
        match_score = score_match.group(1) + "%"

    difficulty_match = re.search(r"(Low|Medium|High)", report_text)
    if difficulty_match:
        hiring_difficulty = difficulty_match.group(1)

# --- Metrics Row ---
metric1, metric2, metric3 = st.columns(3)

vault_data = get_all_vault_resumes()
candidate_count = 0

if vault_data and "documents" in vault_data:
    candidate_count = len(vault_data["documents"])

with metric1:
    st.metric("Candidates Processed", candidate_count)

with metric2:
    st.metric("Match Score", match_score)

with metric3:
    st.metric("Hiring Difficulty", hiring_difficulty)

st.markdown("---")

# --- Sidebar ---
with st.sidebar:

    st.image("https://img.icons8.com/fluency/200/artificial-intelligence.png", width=120)
    st.title("Control Center")

    app_mode = st.radio("Navigation", ["🚀 New Analysis", "🗄️ Resume Vault", "💬 HR Assistant"])

    st.markdown("---")

    model_choice = st.selectbox(
        "Intelligence Engine",
        ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "GPT-4o (Coming Soon)"]
    )

    anonymize_mode = st.toggle("Strict Anonymization", value=True)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =====================================================
# 🚀 NEW ANALYSIS
# =====================================================

if app_mode == "🚀 New Analysis":

    col1, col2 = st.columns([1.2, 3.8], gap="large")

    with col1:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Opportunity")

        default_jd = ""
        jd_path = "data/job_description.md"

        if os.path.exists(jd_path):
            with open(jd_path, "r") as f:
                default_jd = f.read()

        job_desc = st.text_area(
            "Job Description / Role Requirements",
            value=default_jd,
            height=350
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Candidate")

        uploaded_resume = st.file_uploader("Upload Resume", type=["pdf"])
        uploaded_video = st.file_uploader("Upload Intro Video (Optional)", type=["mp4", "mov", "avi"])

        if st.button("Run Intelligence Engine", use_container_width=True):

            if not job_desc or not uploaded_resume:
                st.error("Please provide both a Job Description and a Resume.")

            else:

                try:

                    with open("temp_resume.pdf", "wb") as f:
                        f.write(uploaded_resume.getbuffer())

                    resume_text = extract_text_from_pdf("temp_resume.pdf")

                    crew_result = run_recruitment_flow(
                        resume_text,
                        job_desc
                    )

                    st.session_state.last_result = crew_result
                    st.session_state.current_resume_text = resume_text
                    st.session_state.current_filename = uploaded_resume.name

                except Exception as e:
                    st.error(str(e))

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.last_result:

        st.markdown("## 📊 Strategic Recruitment Dossier")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.last_result.raw)
        st.markdown('</div>', unsafe_allow_html=True)

        icol1, icol2 = st.columns(2)

        with icol1:

            st.download_button(
                label="📥 Download Intelligence Dossier",
                data=str(st.session_state.last_result.raw),
                file_name=f"recruitment_intelligence_{int(time.time())}.md",
                mime="text/markdown"
            )

        with icol2:

            if st.button("💾 Save Candidate to Vault"):

                report_text = str(st.session_state.last_result.raw)

                score_match = re.search(r"(\d+)/100", report_text)
                ai_score = int(score_match.group(1)) if score_match else 0

                meta = {
                    "role": job_desc[:50],
                    "source": st.session_state.get("current_filename", "uploaded_resume"),
                    "ai_score": ai_score,
                    "timestamp": time.time()
                }

                save_to_vault(
                    st.session_state.current_resume_text,
                    meta
                )

                st.toast("Candidate safely archived in Vault!")

# =====================================================
# 🗄️ RESUME VAULT
# =====================================================

elif app_mode == "🗄️ Resume Vault":

    st.markdown("## 🗄️ Talent Archive")

    search_query = st.text_input(
        "🔍 Search Vault",
        placeholder="e.g. React developer with ML experience"
    )

    if search_query:

        results = search_vault(search_query)

        st.subheader(f"Results for: {search_query}")

        if results and results["documents"]:

            for i, doc in enumerate(results["documents"][0]):

                similarity = round(1 - results["distances"][0][i], 2)
                ai_score = results["metadatas"][0][i].get("ai_score", "NA")

                with st.expander(
                    f"📄 Candidate {i+1} | AI Score: {ai_score}% | Search Similarity: {similarity}"
                ):
                    st.caption(f"AI Score: {ai_score}%")
                    st.caption(f"Search Similarity: {similarity}")
                    st.markdown(doc)
                    st.caption(f"Metadata: {results['metadatas'][0][i]}")

        else:
            st.info("No matching candidates found in the vault.")

# =====================================================
# 💬 HR ASSISTANT
# =====================================================

elif app_mode == "💬 HR Assistant":

    st.markdown("## 💬 HR Strategic Assistant")

    if not st.session_state.last_result:
        st.info("Run a new analysis first.")

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Footer ---
st.markdown("""
<div style="text-align:center;color:#F5D5E0;font-size:0.8rem;">
Powered by <b>CrewAI</b> + <b>Google Gemini</b><br>
Built for Ethical & Data-Driven Hiring
</div>
""", unsafe_allow_html=True)

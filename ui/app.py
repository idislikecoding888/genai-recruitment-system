import streamlit as st
import os
import sys
import time

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

:root {
    --primary: #6667AB;
    --secondary: #7B337E;
    --accent: #F5D5E0;
    --background: #210635;
    --card-bg: rgba(66, 13, 75, 0.7);
}

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
    margin-bottom: 0.25rem;
    letter-spacing: -0.05em;
}

.subtitle {
    color: #F5D5E0;
    font-size: 1.1rem;
    margin-bottom: 1.2rem;
    font-weight: 400;
    opacity: 0.85;
}

.stButton>button {
     background: linear-gradient(135deg,#6667AB,#7B337E);
    border-radius:14px;
    font-weight:600;
    font-size:16px;
    padding:0.9rem 2rem;
    box-shadow:0 6px 20px rgba(0,0,0,0.45);
}

.stButton>button:hover {
    transform: translateY(-3px);
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(245,213,224,0.2);
    color: #F5D5E0;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.2);
}

.glass-card {
    background: rgba(66, 13, 75, 0.55);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.45);
    margin-bottom: 1.5rem;
    transition: all 0.2s ease;
}

.glass-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 45px rgba(0,0,0,0.55);
}

     
/* hide empty containers */
.glass-card:empty {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-header">Smart Hire</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Recruitment Intelligence Platform</p>', unsafe_allow_html=True)
import re

match_score = "--"
hiring_difficulty = "Pending"

if "last_result" in st.session_state and st.session_state.last_result:

    report_text = st.session_state.last_result.raw

    # extract score like 85%
    score_match = re.search(r"(\d+)%", report_text)
    if score_match:
        match_score = score_match.group(1) + "%"

    # extract hiring difficulty
    difficulty_match = re.search(r"Hiring Difficulty:\s*(\w+)", report_text)
    if difficulty_match:
        hiring_difficulty = difficulty_match.group(1)
# --- Metrics Row ---
# --- Metrics Row ---

metric1, metric2, metric3 = st.columns(3)

# Get candidate count safely
vault_data = get_all_vault_resumes()
candidate_count = 0

if vault_data and "documents" in vault_data:
    candidate_count = len(vault_data["documents"])

# Default values
match_score = "--"
hiring_difficulty = "Pending"

# Only try extracting if analysis exists
if "last_result" in st.session_state and st.session_state.last_result:
    report_text = str(st.session_state.last_result.raw)

    import re

    score_match = re.search(r"(\d+)%", report_text)
    if score_match:
        match_score = score_match.group(1) + "%"

    difficulty_match = re.search(r"(Low|Medium|High)", report_text)
    if difficulty_match:
        hiring_difficulty = difficulty_match.group(1)

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

    st.markdown("---")
    st.markdown("### Active Agents")

    st.write("TA Manager")
    st.write("Sourcing Agent")
    st.write("Screening Agent")
    st.write("Candidate Experience")
    st.write("Bias Detection")
    st.write("Talent Analytics")
    st.write("Market Predictor")
    st.write("Onboarding")
    st.write("Explainable AI")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# --- Main Layout ---
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
            height=350,
            placeholder="Paste the job description here..."
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.subheader("Candidate")
        st.markdown("#### Upload Resume")
        uploaded_resume = st.file_uploader(
            "Upload Professional Resume",
            type=["pdf"],
            help="Supports specialized PDF parsing"
        )
        st.markdown("#### Upload Introduction Video")
        uploaded_video = st.file_uploader(
            "Upload Intro Video (Optional)",
            type=["mp4", "mov", "avi"],
            help="AI will analyze tone, confidence, and communication style."
        )

        if st.button("Run Intelligence Engine", use_container_width=True):

            if not job_desc or not uploaded_resume:

                st.error("Please provide both a Job Description and a Resume.")

            else:

                try:

                    resume_text = ""
                    video_path = None

                    with st.status("🛠️ System Initializing...", expanded=True) as status:

                        st.write("📄 Parsing PDF Content...")

                        with open("temp_resume.pdf", "wb") as f:
                            f.write(uploaded_resume.getbuffer())

                        resume_text = extract_text_from_pdf("temp_resume.pdf")

                        st.toast("Resume parsed successfully!", icon="✅")

                        if uploaded_video:

                            st.write("🎥 Staging Video bytes...")

                            video_path = f"temp_video_{uploaded_video.name}"

                            with open(video_path, "wb") as f:
                                f.write(uploaded_video.getbuffer())

                            st.success(f"Video '{uploaded_video.name}' attached")

                        st.write("🧠 Consulting TA Strategic Manager...")

                        crew_result = run_recruitment_flow(
                            resume_text,
                            job_desc,
                            video_path=video_path
                        )

                        st.session_state.last_result = crew_result
                        st.session_state.current_resume_text = resume_text
                        st.session_state.current_filename = uploaded_resume.name

                        status.update(
                            label="✅ Full Intelligence Dossier Ready!",
                            state="complete",
                            expanded=False
                        )

                except Exception as e:

                    st.error(f"Engine Failure: {str(e)}")
                    st.exception(e)

    with col2:

        if st.session_state.last_result:

            st.markdown("## 📊 Strategic Recruitment Dossier")

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            st.markdown(st.session_state.last_result.raw)

            st.markdown('</div>', unsafe_allow_html=True)

            st.success(
                "All recruitment modules (Screening, Sourcing, Engagement, and Interview Prep) have been unified into the report above."
            )

            st.markdown("<br>", unsafe_allow_html=True)

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

                    import re

                    report_text = str(st.session_state.last_result.raw)

                    # extract AI score like 86/100
                    score_match = re.search(r"(\d+)/100", report_text)
                    ai_score = int(score_match.group(1)) if score_match else 0

                    meta = {
                        "role": job_desc[:50],
                        "source": st.session_state.get('current_filename', 'uploaded_resume'),
                        "ai_score": ai_score,
                        "timestamp": time.time()
                    }

                    save_to_vault(
                        st.session_state.current_resume_text,
                        meta
                    )

                    st.toast("Candidate safely archived in Vault!")

# --- Resume Vault ---
elif app_mode == "🗄️ Resume Vault":

    st.markdown("## 🗄️ Talent Archive")

    st.markdown(
        '<p class="subtitle">Search and manage your historical talent pool</p>',
        unsafe_allow_html=True
    )

    search_query = st.text_input(
        "🔍 Search Vault",
        placeholder="e.g. Senior Frontend Developer with React experience..."
    )

    if search_query:

        results = search_vault(search_query)

        st.subheader(f"Results for: {search_query}")

        if results and results['documents']:

            for i, doc in enumerate(results['documents'][0]):

                similarity = round(1 - results["distances"][0][i], 2)

                ai_score = results["metadatas"][0][i].get("ai_score")

                if ai_score is None:
                    ai_score_display = "Not Scored"
                else:
                    ai_score_display = f"{ai_score}%"

                with st.expander(
                    f"📄 Candidate {i+1} | AI Score: {ai_score_display} | Search Similarity: {similarity}"
                ):
                    st.markdown(doc)
                    st.caption(f"Metadata: {results['metadatas'][0][i]}")
        else:

            st.info("No matching candidates found in the vault.")

# --- HR Assistant ---
elif app_mode == "💬 HR Assistant":

    st.markdown("## 💬 HR Strategic Assistant")

    st.markdown(
        '<p class="subtitle">Real-time status and strategic insights from your TA Manager</p>',
        unsafe_allow_html=True
    )

    if not st.session_state.last_result:

        st.info(
            "👋 Hello! I am your Talent Acquisition Manager. Run a new analysis first so I can provide insights."
        )

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#F5D5E0;font-size:0.8rem;">
Powered by <b>CrewAI</b> + <b>Google Gemini</b><br>
Built for Ethical & Data-Driven Hiring
</div>
""", unsafe_allow_html=True)
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
    page_title="TalentSpark AI | Recruitment Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Styling ---
# (keeping existing styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --accent: #ec4899;
        --background: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
        color: #f1f5f9;
    }
    
    .main-header {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
        letter-spacing: -0.05em;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        border: none;
        color: white;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    div[data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 1rem;
    }

    div[data-baseweb="tab"] {
        height: 50px;
        background-color: var(--card-bg) !important;
        border-radius: 0.75rem 0.75rem 0 0 !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 0 1.5rem !important;
    }

    div[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%) !important;
        color: white !important;
        border-bottom: 2px solid var(--primary) !important;
    }

    /* Aggressive Full Width & Centering */
    .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-right: 2rem !important;
        padding-left: 2rem !important;
        padding-bottom: 1rem !important;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
    }

    .glass-card {
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.25rem;
        padding: 2.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        width: 100%;
        display: block;
    }

    /* Remove specific streamlit alignment constraints */
    [data-testid="column"] {
        width: 100% !important;
    }

    [data-testid="stHorizontalBlock"] {
        gap: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-header">TalentSpark AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-Gen Agentic Recruitment & Market Intelligence</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/500/shuttle.png", width=150)
    st.title("Control Center")
    
    app_mode = st.radio("Navigation", ["🚀 New Analysis", "🗄️ Resume Vault", "💬 HR Assistant"])
    
    st.markdown("---")
    model_choice = st.selectbox("Intelligence Engine", ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "GPT-4o (Coming Soon)"])
    anonymize_mode = st.toggle("Strict Anonymization", value=True)
    st.markdown("---")
    st.markdown("### Active Agents")
    st.caption("✅ TA Manager (Process Owner)")
    st.caption("✅ Sourcing Agent (Market Intelligence)")
    st.caption("✅ Screening Agent (NLP Assessment)")
    st.caption("✅ Candidate Experience Agent (Engagement & Scheduling)")
    st.caption("🧠 Bias Detection Agent (Fair Hiring)")
    st.caption("📊 Talent Analytics Agent (Hiring Insights)")
    st.caption("📈 Talent Market Predictor (Supply Intelligence)")
    st.caption("📄 Offer & Onboarding Agent")
    st.caption("🔍 Explainable AI Agent (Decision Transparency)")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# --- Main Layout ---
if app_mode == "🚀 New Analysis":
    col1, col2 = st.columns([1, 4], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🎯 Opportunity")
        
        default_jd = ""
        jd_path = "data/job_description.md"
        if os.path.exists(jd_path):
            with open(jd_path, "r") as f:
                default_jd = f.read()
                
        job_desc = st.text_area("Job Description / Role Requirements", value=default_jd, height=350, placeholder="Paste the job description here...")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👤 Candidate")
        uploaded_resume = st.file_uploader("Upload Professional Resume", type=["pdf"], help="Supports specialized PDF parsing")
        uploaded_video = st.file_uploader("Upload Intro Video (Optional)", type=["mp4", "mov", "avi"], help="AI will analyze tone, confidence, and communication style.")
        
        if st.button("🚀 Ignite Intelligence Engine", use_container_width=True):
            if not job_desc or not uploaded_resume:
                st.error("Please provide both a Job Description and a Resume.")
            else:
                try:
                    resume_text = ""
                    video_path = None
                    with st.status("🛠️ System Initializing...", expanded=True) as status:
                        # Process Resume
                        st.write("📄 Parsing PDF Content...")
                        with open("temp_resume.pdf", "wb") as f:
                            f.write(uploaded_resume.getbuffer())
                        resume_text = extract_text_from_pdf("temp_resume.pdf")
                        st.toast("Resume parsed successfully!", icon="✅")
                        
                        # Handle Video
                        if uploaded_video:
                            st.write("🎥 Staging Video bytes...")
                            video_path = f"temp_video_{uploaded_video.name}"
                            with open(video_path, "wb") as f:
                                f.write(uploaded_video.getbuffer())
                            st.success(f"Video '{uploaded_video.name}' attached")
                        
                        st.write("🧠 Consulting TA Strategic Manager...")
                        # Run the flow
                        crew_result = run_recruitment_flow(resume_text, job_desc, video_path=video_path)
                        st.session_state.last_result = crew_result
                        st.session_state.current_resume_text = resume_text
                        st.session_state.current_filename = uploaded_resume.name
                        
                        status.update(label="✅ Full Intelligence Dossier Ready!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Engine Failure: {str(e)}")
                    st.exception(e)

    with col2:
        if st.session_state.last_result:
            # Full Intelligence Report
            st.markdown("## 📊 Strategic Recruitment Dossier")
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(st.session_state.last_result.raw)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.success("All recruitment modules (Screening, Sourcing, Engagement, and Interview Prep) have been unified into the report above.")
            
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
                    from main import save_to_vault
                    # Use first few words of JD as metadata
                    meta = {
                        "role": job_desc[:50], 
                        "source": st.session_state.get('current_filename', 'uploaded_resume'),
                        "timestamp": time.time()
                    }
                    save_to_vault(st.session_state.current_resume_text, meta)
                    st.toast("Candidate safely archived in Vault!")

elif app_mode == "🗄️ Resume Vault":
    st.markdown("## 🗄️ Talent Archive")
    st.markdown('<p class="subtitle">Search and manage your historical talent pool</p>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search Vault", placeholder="e.g. Senior Frontend Developer with React experience...")
    
    if search_query:
        results = search_vault(search_query)
        st.subheader(f"Results for: {search_query}")
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                with st.expander(f"📄 Candidate {i+1} | Match Score: {round(1-results['distances'][0][i], 2)}"):
                    st.markdown(doc)
                    st.caption(f"Metadata: {results['metadatas'][0][i]}")
        else:
            st.info("No matching candidates found in the vault.")
    else:
        st.info("Displaying all candidates in the archive...")
        all_resumes = get_all_vault_resumes()
        if all_resumes and all_resumes['documents'] and len(all_resumes['documents']) > 0:
            for i, doc in enumerate(all_resumes['documents']):
                with st.expander(f"📄 Candidate {i+1}"):
                    st.markdown(doc)
                    st.caption(f"Metadata: {all_resumes['metadatas'][i]}")
            
            st.markdown("---")
            if st.button("🚨 Clear All Resumes from Vault", help="This action is irreversible!"):
                clear_vault()
                st.toast("Vault successfully cleared!", icon="🔥")
                st.rerun()
        else:
            st.warning("The Resume Vault is currently empty. Analyze and save candidates to see them here.")

elif app_mode == "💬 HR Assistant":
    st.markdown("## 💬 HR Strategic Assistant")
    st.markdown('<p class="subtitle">Real-time status and strategic insights from your TA Manager</p>', unsafe_allow_html=True)
    
    if not st.session_state.last_result:
        st.info("👋 Hello! I am your Talent Acquisition Manager. Run a new analysis first so I can provide specific insights on your candidates.")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about the candidate, market trends, or next steps..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting with the recruitment crew..."):
                try:
                    from google import genai
                    from config import GOOGLE_API_KEY
                    
                    client = genai.Client(api_key=GOOGLE_API_KEY)
                    
                    # Provide context from the last analysis
                    context = ""
                    if st.session_state.last_result:
                        context = f"Here is the latest recruitment report context:\n{st.session_state.last_result.raw}"
                    
                    full_prompt = f"""
                    You are the 'Talent Acquisition Manager'. 
                    Your goal is to answer questions from the HR Manager about the recruitment process.
                    
                    {context}
                    
                    User Question: {prompt}
                    """
                    
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=full_prompt
                    )
                    
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Chat Error: {str(e)}")

# --- Footer ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem;">
        Powered by <b>CrewAI</b> + <b>Google Gemini 2.0</b> Engine<br>
        Built for Ethical & Data-Driven Hiring
    </div>
""", unsafe_allow_html=True)

# Intelligent Talent Acquisition Assistant - Implementation Plan

## 🎯 Project Goal
Build an agentic multi-agent system to automate recruitment with a focus on bias-mitigation and deep skill assessment.

## 🏗️ Technical Stack
- **Framework**: CrewAI (Agent Coordination)
- **LLM**: OpenAI GPT-4o / Claude 3.5 (via LiteLLM)
- **Vector DB**: ChromaDB (for Resume RAG)
- **Frontend**: Streamlit (for rapid prototyping and research demonstration)
- **Innovations**:
    1. **Bias-Aware Anonymizer**: Redacts PII before screening.
    2. **Skill-Centric Interviewer**: Conducts preliminary technical checks.
    3. **Multi-modal Insights**: Sentiment/Tone analysis from intro videos.

## 📁 Folder Structure
- `/agents`: Definitions for Talent Manager, Sourcing, Screening, etc.
- `/tools`: Custom tools for PDF parsing, web searching, and video analysis.
- `/data`: Storage for job descriptions and (simulated) resumes.
- `/ui`: Streamlit dashboard code.
- `main.py`: Entry point for the CrewAI orchestration.

## 🚀 Status
- [x] Initial Project Structure
- [x] Gemini API Configuration
- [x] Core Agents (Bias Mitigation, Screening, Interviewer)
- [x] Main Orchestrator (`main.py`)
- [x] Phase 2: Premium Streamlit Dashboard UI (`ui/app.py`)
- [x] Phase 3: Advanced Intelligence (Market Research & Culture Fit)
- [x] Phase 4: Resume Vault (ChromaDB RAG Integration)
- [x] Phase 5: Multi-modal Support (Video Behavior Analysis)
- [x] Phase 6: Automated Talent Sourcing (Web Sourcing Agent)
- [x] Phase 7: Candidate Engagement & Scheduling
- [x] Phase 8: HR Strategic Assistant (Conversational Chatbot)

## 🏃 How to Run
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup API Key**:
   - Create a `.env` file.
   - Add `GOOGLE_API_KEY=your_key_here`.
3. **Execute**:
   ```bash
   python main.py
   ```

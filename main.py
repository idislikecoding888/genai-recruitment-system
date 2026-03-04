import os
from crewai import Crew, Process, Task
from agents.recruitment_agents import RecruitmentAgents
import time

def run_recruitment_flow(resume_text, job_description, video_path=None):
    """
    STABLE MULTI-AGENT FLOW:
    Uses 4 specialized agents defined by the user.
    """
    agents = RecruitmentAgents()
    
    # Initialize agents
    manager = agents.talent_acquisition_manager()
    sourcer = agents.sourcing_agent()
    screener = agents.screening_agent()
    coordinator = agents.engagement_scheduling_agent()

    # Define Video Insight Context
    video_summary = ""
    if video_path and os.path.exists(video_path):
        from tools.video_processor import analyze_video
        video_summary = f"\n[VIDEO INSIGHTS]: {analyze_video(video_path, 'Summarize the candidate tone and confidence.')}"

    # 1. Sourcing Task
    sourcing_task = Task(
        description=f"Research and cite 3 alternate candidate profiles or market benchmarks similar to this role: {job_description}",
        expected_output="A list of 3 candidate profiles/links and skill rarity analysis.",
        agent=sourcer
    )

    # 2. Screening Task
    screening_task = Task(
        description=f"Analyze this resume: {resume_text} against the JD: {job_description}. {video_summary}",
        expected_output="Anonymized resume snippets, technical fit score (0-100), and skill gap analysis.",
        agent=screener
    )

    # 3. Engagement & Scheduling Task
    engagement_task = Task(
        description="""Draft a personalized outreach email based on the screening results. 
        Also, propose an interview roadmap including 3 architectural questions and potential time slots.""",
        expected_output="A personalized email and a structured interview plan with logic questions.",
        agent=coordinator
    )

    # 4. Management & Synthesis Task
    management_task = Task(
        description="""Review the output from the Sourcing, Screening, and Engagement tasks. 
        Synthesize everything into a final 'Strategic Recruitment Dossier' for the HR Director.""",
        expected_output="A comprehensive final report containing Sourcing, Screening, Engagement, and Interview plans.",
        agent=manager,
        context=[sourcing_task, screening_task, engagement_task]
    )

    # Create Crew
    recruitment_crew = Crew(
        agents=[manager, sourcer, screener, coordinator],
        tasks=[sourcing_task, screening_task, engagement_task, management_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute
    return recruitment_crew.kickoff()

def save_to_vault(resume_text, metadata):
    from tools.rag_processor import vault
    return vault.add_resume(resume_text, metadata)

def search_vault(query):
    from tools.rag_processor import vault
    return vault.search_similar_resumes(query)

def get_all_vault_resumes():
    from tools.rag_processor import vault
    return vault.get_all_resumes()

def clear_vault():
    from tools.rag_processor import vault
    return vault.clear_vault()

if __name__ == "__main__":
    pass

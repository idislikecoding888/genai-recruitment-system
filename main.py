import os
from crewai import Crew, Process, Task
from agents.recruitment_agents import RecruitmentAgents
import time


def run_recruitment_flow(resume_text, job_description, video_path=None):
    """
    EXTENDED MULTI-AGENT RECRUITMENT FLOW
    Includes fairness, analytics, market intelligence,
    onboarding automation, and explainable AI.
    """

    agents = RecruitmentAgents()

    # Core agents
    manager = agents.talent_acquisition_manager()
    sourcer = agents.sourcing_agent()
    screener = agents.screening_agent()
    coordinator = agents.engagement_scheduling_agent()

    # New intelligent agents
    fairness = agents.fairness_agent()
    analytics = agents.analytics_agent()
    market_predictor = agents.market_predictor_agent()
    onboarding = agents.onboarding_agent()
    explainer = agents.explainability_agent()

    # Video insight context
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

    # 3. Bias Detection Task
    fairness_task = Task(
        description="Analyze the screening output and detect potential bias in hiring evaluation such as gender, college, or experience bias.",
        expected_output="Bias risk score and flagged hiring biases if present.",
        agent=fairness,
        context=[screening_task]
    )

    # 4. Market Prediction Task
    market_task = Task(
        description=f"Analyze the hiring market for this role: {job_description}. Predict hiring difficulty, talent supply, and estimated hiring timeline.",
        expected_output="Market supply level, competition level, and estimated time to hire.",
        agent=market_predictor
    )

    # 5. Engagement & Scheduling Task
    engagement_task = Task(
        description="""Draft a personalized outreach email based on the screening results. 
        Also, propose an interview roadmap including 3 architectural questions and potential time slots.""",
        expected_output="A personalized email and a structured interview plan with logic questions.",
        agent=coordinator,
        context=[screening_task]
    )

    # 6. Analytics Task
    analytics_task = Task(
        description="Generate hiring insights including candidate drop-off risks, best sourcing channels, and predicted hiring efficiency.",
        expected_output="Hiring insights report with metrics like time-to-hire and sourcing effectiveness.",
        agent=analytics,
        context=[sourcing_task, screening_task]
    )

    # 7. Offer & Onboarding Task
    onboarding_task = Task(
        description="Prepare a suggested offer package and onboarding checklist based on the candidate screening results.",
        expected_output="Offer recommendation including salary benchmark and onboarding checklist.",
        agent=onboarding,
        context=[screening_task]
    )

    # 8. Management & Strategic Report
    management_task = Task(
        description="""Review outputs from sourcing, screening, fairness analysis, engagement planning, 
        market intelligence, analytics, and onboarding recommendations.

        Synthesize everything into a final 'Strategic Recruitment Dossier' for the HR Director.""",
        expected_output="A comprehensive final report containing sourcing insights, screening evaluation, fairness analysis, engagement strategy, hiring analytics, and offer recommendation.",
        agent=manager,
        context=[
            sourcing_task,
            screening_task,
            fairness_task,
            engagement_task,
            market_task,
            analytics_task,
            onboarding_task
        ]
    )

    # 9. Explainability Task
    explainability_task = Task(
        description="Explain clearly why the candidate is recommended or rejected based on screening results.",
        expected_output="Transparent explanation including skill mismatch, experience gap, and hiring reasoning.",
        agent=explainer,
        context=[screening_task]
    )

    # Create Crew
    recruitment_crew = Crew(
        agents=[
            manager,
            sourcer,
            screener,
            coordinator,
            fairness,
            analytics,
            market_predictor,
            onboarding,
            explainer
        ],
        tasks=[
            sourcing_task,
            screening_task,
            fairness_task,
            market_task,
            engagement_task,
            analytics_task,
            onboarding_task,
            management_task,
            explainability_task
        ],
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

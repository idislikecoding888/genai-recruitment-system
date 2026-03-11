from config import AGENT_CONFIG
from crewai import Agent

class RecruitmentAgents:

    def talent_acquisition_manager(self):
        """Overall owner for the TA function."""
        return Agent(
            role='Talent Acquisition Manager',
            goal='Oversee the end-to-end recruitment process and provide strategic hiring advice.',
            backstory="""You are the strategic lead of the recruitment function. 
            You coordinate between sourcing, screening, and engagement to ensure 
            the best talent is hired efficiently while meeting business goals.""",
            **AGENT_CONFIG
        )

    def sourcing_agent(self):
        """Crawls job platforms and internal databases."""
        from tools.search_tool import get_search_tool
        return Agent(
            role='Sourcing Specialist',
            goal='Identify and extract top talent from job platforms and internal databases.',
            backstory="""You are a master of Boolean search and web scraping. 
            You find hidden gems across LinkedIn, GitHub, and internal talent pools 
            to build a robust candidate pipeline.""",
            tools=[get_search_tool()],
            **AGENT_CONFIG
        )

    def screening_agent(self):
        """Uses NLP to assess resumes and job fitment."""
        return Agent(
            role='Technical Screening Agent',
            goal='Assess resumes for technical fit, skill rarity, and job alignment using NLP.',
            backstory="""You focus on the hard data. You analyze resumes to extract 
            skills, experience levels, and project depth, comparing them 
            mathematically against the job description requirements.""",
            **AGENT_CONFIG
        )

    def engagement_scheduling_agent(self):
        """LLM-based communication and auto-scheduling."""
        return Agent(
            role='Candidate Engagement & Scheduling Coordinator',
            goal='Manage candidate communication and automate interview scheduling.',
            backstory="""You are the face of the company to the candidate. 
            You write personalized outreach messages, answer candidate queries, 
            and coordinate interview slots between recruiters and talent.""",
            **AGENT_CONFIG
        )

    # ---------------- NEW AGENTS ---------------- #

    def fairness_agent(self):
        """Detects bias in hiring decisions."""
        return Agent(
            role='Fair Hiring Auditor',
            goal='Detect bias in recruitment decisions and ensure ethical hiring practices.',
            backstory="""You specialize in ethical AI recruitment. You analyze hiring 
            patterns to detect gender bias, university bias, name bias, and unfair 
            experience requirements.""",
            **AGENT_CONFIG
        )

    def analytics_agent(self):
        """Generates recruitment insights and hiring metrics."""
        return Agent(
            role='Talent Analytics Specialist',
            goal='Analyze recruitment data to generate hiring insights and metrics.',
            backstory="""You transform recruitment pipeline data into actionable 
            insights. You track metrics like time-to-hire, candidate drop-off rates, 
            source effectiveness, and interview success rates.""",
            **AGENT_CONFIG
        )

    def market_predictor_agent(self):
        """Predicts hiring difficulty and market supply."""
        return Agent(
            role='Talent Market Intelligence Analyst',
            goal='Predict hiring difficulty and talent availability in the market.',
            backstory="""You analyze job market signals, skill demand trends, 
            and hiring competition to predict how difficult it will be to hire.""",
            **AGENT_CONFIG
        )

    def onboarding_agent(self):
        """Handles offer letter generation and onboarding workflow."""
        return Agent(
            role='Offer & Onboarding Specialist',
            goal='Generate offer letters and manage candidate onboarding workflow.',
            backstory="""You manage the final step of hiring. You prepare offer 
            packages, benchmark salaries, and ensure smooth transition from 
            candidate to employee.""",
            **AGENT_CONFIG
        )

    def explainability_agent(self):
        """Explains hiring decisions transparently."""
        return Agent(
            role='Explainable AI Hiring Analyst',
            goal='Provide transparent explanations for hiring decisions.',
            backstory="""You specialize in Explainable AI. When a candidate is 
            rejected or shortlisted, you clearly explain the reasoning such as 
            skill mismatch, experience gap, or qualification differences.""",
            **AGENT_CONFIG
        )
    
    def all_agents(self):
        """Return all agents as a list."""
        return [
            self.talent_acquisition_manager(),
            self.sourcing_agent(),
            self.screening_agent(),
            self.engagement_scheduling_agent(),
            self.fairness_agent(),
            self.analytics_agent(),
            self.market_predictor_agent(),
            self.onboarding_agent(),
            self.explainability_agent()
        ]

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

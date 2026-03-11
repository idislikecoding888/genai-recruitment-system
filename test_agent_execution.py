from agents.recruitment_agents import RecruitmentAgents
from crewai import Task, Crew

agents = RecruitmentAgents()

screening_agent = agents.screening_agent()

task = Task(
    description="Evaluate a candidate resume: Python developer with 3 years experience in machine learning and APIs.",
    expected_output="A short evaluation of the candidate's technical fit.",
    agent=screening_agent
)

crew = Crew(
    agents=[screening_agent],
    tasks=[task]
)

result = crew.kickoff()

print("\nAgent execution result:\n")
print(result)
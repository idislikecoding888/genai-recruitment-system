from agents.recruitment_agents import RecruitmentAgents

agents = RecruitmentAgents()

for agent in agents.all_agents():
    print("Agent created:", agent.role)
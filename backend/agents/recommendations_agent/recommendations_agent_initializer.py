from backend.agents.recommendations_agent.recommendations_agent import RecommendationsAgent


if RecommendationsAgent.recommendations_agent_exists():
    RECOMMENDATIONS_AGENT = RecommendationsAgent.get_recommendations_agent()
    print("Recommendations agent wasn't created")  # TODO remove
else:
    pass
    #RECOMMENDATIONS_AGENT = RecommendationsAgent()
    print("Recommendations agent was created")  # TODO remove

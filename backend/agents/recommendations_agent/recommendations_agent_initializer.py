from backend.agents.recommendations_agent.recommendations_agent import RecommendationsAgent


if RecommendationsAgent.recommendations_agent_exists():
    RECOMMENDATIONS_AGENT = RecommendationsAgent.get_recommendations_agent()
    print("Recommendations agent wasn't created")  # TODO remove
else:

    test_recommendations_agent_coefficients = {
        "main_categories_names": 1.0,
        "subcategories_names": 1.0,
        "distance": -1.0,
        "wish_to_visit": 1.0,
        "visited_amount": -1.0
    }

    RECOMMENDATIONS_AGENT = RecommendationsAgent(test_recommendations_agent_coefficients)
    print("Recommendations agent was created")  # TODO remove

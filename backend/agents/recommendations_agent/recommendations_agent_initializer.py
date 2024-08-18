from backend.agents.recommendations_agent.recommendations_agent import RecommendationsAgent
import torch


if RecommendationsAgent.recommendations_agent_exists():
    RECOMMENDATIONS_AGENT = RecommendationsAgent.get_recommendations_agent()
    print("Recommendations agent wasn't created")  # TODO remove
else:
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    dtype = torch.float32
    RECOMMENDATIONS_AGENT = RecommendationsAgent()
    print("Recommendations agent was created")  # TODO remove

from backend.agents.recommendations_agent.trainer_agent import TrainerAgent


if TrainerAgent.trainer_agent_exists():
    TRAINER_AGENT = TrainerAgent.get_trainer_agent()
    print("Trainer agent wasn't created")  # TODO remove
else:
    pass
    #TRAINER_AGENT = RecommendationsAgent()
    print("Trainer agent was created")  # TODO remove
from backend.agents.landmarks_by_sectors_agent.landmarks_by_sectors_agent import LandmarksBySectorsAgent

if LandmarksBySectorsAgent.landmarks_by_sectors_agent_exists():
    LANDMARKS_BY_SECTORS_AGENT = LandmarksBySectorsAgent.get_landmarks_by_sectors_agent()
else:
    LANDMARKS_BY_SECTORS_AGENT = LandmarksBySectorsAgent()

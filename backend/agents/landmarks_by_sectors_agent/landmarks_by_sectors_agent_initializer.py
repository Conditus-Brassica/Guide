from backend.agents.landmarks_by_sectors_agent.landmarks_by_sectors_agent import LandmarksBySectorsAgent
import asyncio
from backend.agents.crud_agent.crud_initializer import CRUD_AGENT

# Define LANDMARKS_BY_SECTORS_AGENT as a global variable
LANDMARKS_BY_SECTORS_AGENT = None

if LandmarksBySectorsAgent.landmarks_by_sectors_agent_exists():
    LANDMARKS_BY_SECTORS_AGENT = LandmarksBySectorsAgent.get_landmarks_by_sectors_agent()
    print("Agent LandmarksBySectors was not created")  # TODO remove
else:
    LANDMARKS_BY_SECTORS_AGENT = LandmarksBySectorsAgent().create()
    print(f"LandmarksBySectors was created")  # TODO remove


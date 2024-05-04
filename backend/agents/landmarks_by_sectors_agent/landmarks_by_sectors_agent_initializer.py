from backend.agents.landmarks_by_sectors_agent.landmarks_by_sectors_agent import LandmarksBySectorsAgent
import asyncio
from backend.agents.crud_agent.crud_initializer import CRUD_AGENT

# Define LANDMARKS_BY_SECTORS_AGENT as a global variable
LANDMARKS_BY_SECTORS_AGENT = None


async def create_landmarks_by_sectors_agent():
    global LANDMARKS_BY_SECTORS_AGENT

    if LandmarksBySectorsAgent.landmarks_by_sectors_agent_exists():
        try:
            LANDMARKS_BY_SECTORS_AGENT = LandmarksBySectorsAgent.get_landmarks_by_sectors_agent()
            print("Agent LandmarksBySectors exists")
        except Exception as e:
            print(f"Error occurred while getting existing agent: {e}")
            # Handle the error as needed
    else:
        try:
            if CRUD_AGENT.crud_exists():
                LANDMARKS_BY_SECTORS_AGENT = await LandmarksBySectorsAgent.create()
                print("LandmarksBySectors was created")
        except Exception as e:
            print(f"Error occurred while creating new agent: {e}")
            # Handle the error as needed


# Call the async function within an event loop and set LANDMARKS_BY_SECTORS_AGENT
async def main():
    global LANDMARKS_BY_SECTORS_AGENT
    await create_landmarks_by_sectors_agent()
    print("Landmarks agent:", LANDMARKS_BY_SECTORS_AGENT)


asyncio.run(main())


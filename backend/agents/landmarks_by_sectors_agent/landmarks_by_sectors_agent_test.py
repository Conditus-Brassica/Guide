import asyncio
import backend.broker.agents_tasks.landmarks_by_sectors_agent_tasks as landmarks_tasks
from pprint import pprint
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_broker import AgentsBroker

"""
Read documentation and description of testing in recommendations_test.py
"""
if __name__ == '__main__':
    async def test():
        await AgentsBroker.get_broker().startup()

        landmarks_sectors_asyncio_task_1 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                landmarks_tasks.get_landmarks_in_sector_task,
                {
                    "TL": {
                        "latitude": 56.232289,
                        "longitude": 23.690447875
                    },
                    "BR": {
                        "latitude": 53.113400874999996,
                        "longitude": 25.5222235
                    }
                }
            )
        )
        landmarks_sectors_asyncio_task_2 = asyncio.create_task(AbstractAgentsBroker.call_agent_task(
            landmarks_tasks.get_landmarks_by_categories_in_sector_task,
            {
                "TL": {
                    "latitude": 56.232289,
                    "longitude": 23.690447875
                },
                "BR": {
                    "latitude": 53.113400874999996,
                    "longitude": 25.5222235
                 },
                "categories_names": ["Музей", "Театр"]
                }
            )
        )

        res11 = await landmarks_sectors_asyncio_task_1
        res12 = await landmarks_sectors_asyncio_task_2

        pprint(res11.return_value)
        pprint(res12.return_value)
        await AgentsBroker.get_broker().shutdown()


    # with open("basic_login.json", 'r') as fout:
    #     basic_login = json.load(fout)
    #

    asyncio.run(test())

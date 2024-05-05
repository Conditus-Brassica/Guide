# Author: Vodohleb04

import asyncio
import datetime

import backend.broker.agents_tasks.crud_agent_tasks as crud_tasks
from pprint import pprint
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_broker import AgentsBroker


if __name__ == '__main__':

    #async def test(login, password):
    async def test():

        # Starting Broker listening (Such code will be located in main, not in agent)
        await AgentsBroker.get_broker().startup()


        # This this emulation of code from another agent
        # Async tasks that kicks broker tasks
        create_user_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.post_user_task,
                {"user_login": "Test user"}
            )
        )

        create_note_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.post_note_task,
                {
                    "guide_login": "Алан Смити",
                    "country_names": ["Беларусь"],
                    "title": "Test title",
                    "category_names": ["Test category"]
                }
            )
        )

        res1 = await create_user_asyncio_task
        res2 = await create_note_asyncio_task
        pprint(res1.return_value)
        pprint(res2.return_value)

        create_route_for_note_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.post_route_for_note_task,
                {
                    "note_title": "Test title",
                    "landmark_info_position_dicts": [
                        {"name": "свирь", "position": 0, "latitude": 54.8069, "longitude": 26.4744},
                        {"name": "нарочь", "position": 1, "latitude": 54.8525, "longitude": 26.7497},
                        {"name": "рудаково", "position": 2, "latitude": 54.8964, "longitude": 26.8922}
                    ]
                }
            )
        )
        #
        # create_route_saved_by_user_asyncio_task = asyncio.create_task(
        #     AbstractAgentsBroker.call_agent_task(
        #         crud_tasks.post_route_saved_by_user_task,
        #         {
        #             "user_login": "Test user",
        #             "landmarks_name_position_pair": [
        #                 {"name": "бабинец (заказник)", "position": 0},
        #                 {"name": "бабиновичский", "position": 1},
        #                 {"name": "болото мох (белоруссия)", "position": 2}
        #             ]
        #         }
        #     )
        # )

        # create_saved_route_from_note_relationship_asyncio_task = asyncio.create_task(
        #     AbstractAgentsBroker.call_agent_task(
        #         crud_tasks.post_saved_route_from_note_relationship_task,
        #         {"user_login": "Test user", "note_title": "Test title"}
        #     )
        # )


        # res3 = await create_route_for_note_asyncio_task
        # res4 = await create_route_saved_by_user_asyncio_task May be an exception because of unique constraint - everything is fine in such case
        #
        res3 = await create_route_for_note_asyncio_task
        pprint(res3.return_value)

        create_route_saved_by_user_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.post_route_saved_by_user_task,
                {
                    "user_login": "Test user",
                    "landmark_info_position_dicts": [
                        {"name": "свирь", "position": 0, "latitude": 54.8069, "longitude": 26.4744},
                        {"name": "нарочь", "position": 1, "latitude": 54.8525, "longitude": 26.7497},
                        {"name": "рудаково", "position": 2, "latitude": 54.8964, "longitude": 26.8922}
                    ]
                }
            )
        )
        create_saved_route_from_note_relationship_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.post_saved_relationship_for_existing_route,
                {"user_login": "Test user", "index_id": 5}
            )
        )

        res4 = await create_route_saved_by_user_asyncio_task
        res5 = await create_saved_route_from_note_relationship_asyncio_task

        #pprint(res3.return_value)
        pprint(res4.return_value)
        pprint(res5.return_value)




        # Closing Broker listeting (Such code will be located in main, not in agent)
        await AgentsBroker.get_broker().shutdown()

        # Closing connection to kb (Such code will be located in main, not in agent)
        from backend.agents.crud_agent.crud_agent import CRUDAgent
        await CRUDAgent.close()


    # with open("basic_login.json", 'r') as fout:
    #     basic_login = json.load(fout)
    #


    asyncio.run(test())
    #asyncio.run(test(basic_login["login"], basic_login["password"]))
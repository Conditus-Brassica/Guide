#Author: Vodohleb04
import asyncio
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
        categories_of_region_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.categories_of_region_task,
                {"region_name": "Мядзельскі раён"}
            )
        )
        landmarks_in_map_sectors_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_in_map_sectors_task,
                {"map_sectors_names": ["a1", "a2", "g2"], "optional_limit": 3}
            )
        )
        landmarks_refers_to_categories_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_refers_to_categories_task,
                {
                    "categories_names": ["озёра мядельского района", "национальные парки белоруссии"],
                    "optional_limit": 3
                }
            )
        )
        landmarks_by_coordinates_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_by_coordinates_task,
                {
                    "coordinates": [
                        {"longitude": 26.91887917, "latitude": 54.84001},
                        {"longitude": 26.8629, "latitude": 54.955}, {"longitude": 26.8684, "latitude": 54.9683}
                    ],
                    "optional_limit": 3
                }
            )
        )
        landmarks_by_names_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_by_names_task,
                {"landmark_names": ["свирь", "рудаково", "нарочь"], "optional_limit": 3}
            )
        )
        landmarks_of_categories_in_region_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_of_categories_in_region_task,
                {"region_name": "Мядзельскі раён", "categories_names": ["национальные парки белоруссии"]}
            )
        )
        landmarks_by_region_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_by_region_task,
                {"region_name": "Мядзел", "optional_limit": 3}
            )
        )
        recommendations_for_landmark_by_region_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.crud_recommendations_for_landmark_by_region_task,
                {
                    "user_login": "user",
                    "current_latitude": 54.8964,
                    "current_longitude": 26.8922,
                    "current_name": "рудаково (озеро)",
                    "amount_of_recommendations": 10
                   }
            )
        )
        map_sectors_of_points_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.map_sectors_of_points_task,
                {
                    "coordinates_of_points": [
                    {"latitude": 55.7, "longitude": 26.7},
                        {"latitude": 55.61639, "longitude": 26.70833},
                        {"latitude": 55.39417, "longitude": 26.62722}
                    ],
                    "optional_limit": 1
                }
            )
        )
        map_sectors_structure_of_region_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.map_sectors_structure_of_region,
                {
                    "region_name": "Беларусь"
                }
            )
        )
        landmarks_of_categories_in_map_sectors_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_of_categories_in_map_sectors_task,
                {
                    "map_sectors_names": ["a8", "h4"],
                    "categories_names": [
                        "историко-культурные ценности республики беларусь",
                        "заказники белоруссии",
                        "озёра поставского района"
                    ],
                    "optional_limit": 1
                }
            )
        )
        recommendations_by_coordinates_and_categories_asyncio_task_1 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.crud_recommendations_by_coordinates_and_categories_task,
                {
                    "coordinates_of_points": [
                        {"latitude": 55.19861, "longitude": 27.41694},
                        {"latitude": 54.1275, "longitude": 25.36306}
                    ],
                    "categories_names": ["озёра поставского района"],
                    # ["историко-культурные ценности республики беларусь", "озёра поставского района"],
                    "user_login": "user",
                    "amount_of_recommendations_for_point": 3,
                    "amount_of_additional_recommendations_for_point": 3,
                    "optional_limit": 6
                }
            )
        )
        recommendations_by_coordinates_and_categories_asyncio_task_2 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.crud_recommendations_by_coordinates_and_categories_task,
                {
                    "coordinates_of_points": [
                        {"latitude": 55.19861, "longitude": 27.41694},
                        {"latitude": 54.1275, "longitude": 25.36306}
                    ],
                    "categories_names": ["озёра поставского района"],
                    # ["историко-культурные ценности республики беларусь", "озёра поставского района"],
                    "user_login": "user",
                    "amount_of_recommendations_for_point": 3,
                    "amount_of_additional_recommendations_for_point": 3,
                    "optional_limit": 6
                }
            )
        )


        # Async tasks running
        res11 = await recommendations_by_coordinates_and_categories_asyncio_task_1
        res11_2 = await recommendations_by_coordinates_and_categories_asyncio_task_2

        res1 = await categories_of_region_asyncio_task
        res2 = await landmarks_in_map_sectors_asyncio_task
        res3 = await landmarks_refers_to_categories_asyncio_task
        res4 = await landmarks_by_coordinates_asyncio_task
        res5 = await landmarks_by_names_asyncio_task
        res6 = await landmarks_of_categories_in_region_asyncio_task
        res7 = await landmarks_by_region_asyncio_task
        res8 = await recommendations_for_landmark_by_region_asyncio_task
        res9 = await map_sectors_of_points_asyncio_task
        res10 = await landmarks_of_categories_in_map_sectors_asyncio_task
        res12 = await map_sectors_structure_of_region_task

        # Taking and printing the result of broker tasks
        pprint(res11.return_value)
        pprint(res11_2.return_value)

        pprint(res1.return_value)
        pprint(res2.return_value)
        pprint(res3.return_value)
        pprint(res4.return_value)
        pprint(res5.return_value)
        pprint(res6.return_value)
        pprint(res7.return_value)
        pprint(res8.return_value)
        pprint(res9.return_value)
        pprint(res10.return_value)
        pprint(res12.return_value)


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
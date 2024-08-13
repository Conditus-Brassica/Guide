#Author: Vodohleb04
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
                crud_tasks.landmarks_by_name_list_task,
                {"landmark_names": ["свирь", "рудаково", "нарочь"]}
            )
        )
        landmarks_by_name_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.landmarks_by_name_task,
                {"landmark_name": "мин", "limit": 3}
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
                crud_tasks.map_sectors_structure_of_region_task,
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
                    "optional_limit": 6
                }
            )
        )

        recommendations_by_coordinates_and_categories_asyncio_task_3 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.crud_recommendations_by_coordinates_and_categories_task,
                {
                    'user_login': '',
                    'coordinates_of_points': [
                        {'latitude': 53.9124414, 'longitude': 27.5951789}
                    ],
                    'categories_names': ['историко-культурные ценности республики беларусь',
                         'историко-культурные ценности республики беларусь', 'памятники истории белоруссии',
                         'памятники истории белоруссии', 'исторические музеи белоруссии',
                         'исторические музеи белоруссии', 'художественные музеи белоруссии',
                         'художественные музеи белоруссии', 'дома-музеи белоруссии', 'дома-музеи белоруссии',
                         'музеи-квартиры белоруссии', 'музеи-квартиры белоруссии',
                         'персональные музеи белоруссии', 'персональные музеи белоруссии',
                         'национальные музеи белоруссии', 'национальные музеи белоруссии',
                         'железнодорожные музеи белоруссии', 'железнодорожные музеи белоруссии',
                         'музеи брестской области', 'музеи брестской области', 'музеи витебской области',
                         'музеи витебской области', 'музеи гомельской области', 'музеи гомельской области',
                         'музеи гродненской области', 'музеи гродненской области', 'музеи могилёвской области',
                         'музеи могилёвской области', 'театры минска', 'театры минска', 'театры гомеля',
                         'театры гомеля', 'театры витебска', 'театры витебска', 'театры бреста',
                         'театры бреста', 'театры белоруссии', 'театры белоруссии', 'сады и парки белоруссии',
                         'сады и парки белоруссии', 'сады и парки минска', 'сады и парки минска',
                         'сады и парки могилёва', 'сады и парки могилёва', 'скверы белоруссии',
                         'скверы белоруссии', 'памятники садово-паркового искусства белоруссии',
                         'памятники садово-паркового искусства белоруссии'],
                    "amount_of_recommendations_for_point": 50,
                    "optional_limit": 40
                }
            )
        )

        route_landmarks_by_index_id_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.route_landmarks_by_index_id_task,
                {'index_id': 6}
            )
        )

        routes_saved_by_user_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.routes_saved_by_user_task,
                {"user_login": 'Test'}
            )
        )
        range_of_routes_saved_by_user_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.range_of_routes_saved_by_user_task,
                {
                    "user_login": 'Test',
                    "skip": 1,
                    "limit": 3
                }
            )
        )
        note_by_title_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.note_by_title_task,
                {
                    "note_title": 'Test title'
                }
            )
        )
        notes_in_range_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.notes_in_range_task,
                {
                    "skip": 0,
                    "limit": 2
                }
            )
        )
        notes_of_categories_in_range_asyncio_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                crud_tasks.notes_of_categories_in_range,
                {
                    "note_categories_names": ["Test category", "категория_2"],
                    "skip": 0,
                    "limit": 2
                }
            )
        )


        # Async tasks running
        res11 = await recommendations_by_coordinates_and_categories_asyncio_task_1
        res11_2 = await recommendations_by_coordinates_and_categories_asyncio_task_2

        start = datetime.datetime.now()
        res11_3 = await recommendations_by_coordinates_and_categories_asyncio_task_3
        print(datetime.datetime.now() - start)
        res1 = await categories_of_region_asyncio_task
        res2 = await landmarks_in_map_sectors_asyncio_task
        res3 = await landmarks_refers_to_categories_asyncio_task
        res4 = await landmarks_by_coordinates_asyncio_task
        res5 = await landmarks_by_names_asyncio_task
        res5_1 = await landmarks_by_name_asyncio_task
        res6 = await landmarks_of_categories_in_region_asyncio_task
        res7 = await landmarks_by_region_asyncio_task
        res8 = await recommendations_for_landmark_by_region_asyncio_task
        res9 = await map_sectors_of_points_asyncio_task
        res10 = await landmarks_of_categories_in_map_sectors_asyncio_task
        res12 = await map_sectors_structure_of_region_task

        res13 = await route_landmarks_by_index_id_asyncio_task
        res14 = await routes_saved_by_user_asyncio_task
        res15 = await range_of_routes_saved_by_user_asyncio_task
        res16 = await note_by_title_asyncio_task
        res17 = await notes_in_range_asyncio_task
        res18 = await notes_of_categories_in_range_asyncio_task


        # Taking and printing the result of broker tasks
        print("\n\nres11")
        pprint(res11.return_value)
        print("\n\nres11_2")
        pprint(res11_2.return_value)

        print("Hard task\n###")
        print("\n\nres11_3")
        pprint(res11_3.return_value)
        print("###")

        res12_return_value = res12.return_value
        print("\n\nres1")
        pprint(res1.return_value)
        print("\\res2")
        pprint(res2.return_value)
        print("\n\nres3")
        pprint(res3.return_value)
        print("\n\nres4")
        pprint(res4.return_value)
        print("\n\nres5")
        pprint(res5.return_value)
        print("\n\nres5_1")
        pprint(res5_1.return_value)
        print("\n\nres6")
        pprint(res6.return_value)
        print("\n\nres7")
        pprint(res7.return_value)
        print("\n\nres8")
        pprint(res8.return_value)
        print("\n\nres9")
        pprint(res9.return_value)
        print("\n\nres10")
        pprint(res10.return_value)
        print("\n\nres12")
        pprint(res12_return_value)
        pprint(len(res12_return_value))

        print("\n\nres13")
        pprint(res13.return_value)
        print("\n\nres14")
        pprint(res14.return_value)
        print("\n\nres15")
        pprint(res15.return_value)
        print("\n\nres16")
        pprint(res16.return_value)
        try:
            pprint(type(res16.return_value[0]["note"]["last_update"]))
        except IndexError:
            print("No notes by title")
        print("\n\nres17")
        pprint(res17.return_value)
        print("\n\nres18")
        pprint(res18.return_value)



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
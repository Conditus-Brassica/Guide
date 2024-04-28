#Author: Vodohleb04
import asyncio
import backend.broker.agents_tasks.recommendations_agent_tasks as recommendations_tasks
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

        recommendations_asyncio_task_1 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                recommendations_tasks.find_recommendations_for_coordinates_and_categories_task,
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
                    "optional_limit": 6,
                    "maximum_amount_of_additional_recommendations": 1,
                    "maximum_amount_of_recommendations": 1
                }
            )
        )
        recommendations_asyncio_task_2 = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                recommendations_tasks.find_recommendations_for_coordinates_and_categories_task,
                {
                    "coordinates_of_points": [
                        {"latitude": 55.19861, "longitude": 27.41694},
                        {"latitude": 54.1275, "longitude": 25.36306}
                    ],
                    "categories_names": ["озёра поставского района"],
                    # ["историко-культурные ценности республики беларусь", "озёра поставского района"],
                    "user_login": "user",
                    "amount_of_recommendations_for_point": 3,
                    "optional_limit": 20,
                    "maximum_amount_of_recommendations": 15
                }
            )
        )


        # Async tasks running
        res11 = await recommendations_asyncio_task_1
        res11_2 = await recommendations_asyncio_task_2


        # Taking and printing the result of broker tasks
        pprint(res11.return_value)
        pprint(res11_2.return_value)



        # Closing Broker listeting (Such code will be located in main, not in agent)
        await AgentsBroker.get_broker().shutdown()


    # with open("basic_login.json", 'r') as fout:
    #     basic_login = json.load(fout)
    #


    asyncio.run(test())
    #asyncio.run(test(basic_login["login"], basic_login["password"]))


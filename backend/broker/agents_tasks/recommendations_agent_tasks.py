# Author: Vodohleb04
"""Tasks to work with recommendations agent. Use broker to run tasks"""
from typing import Dict
from ..broker_initializer import BROKER
from backend.agents.recommendations_agent.recommendations_agent_initializer import RECOMMENDATIONS_AGENT


@BROKER.task
async def find_recommendations_for_coordinates_and_categories_task(json_params: Dict):
    """
    Task to get the recommendations (landmarks) that located nearby the given coordinates and refers to the given
    categories for the given user.

    Do NOT call this task directly. Give it as the first argument (agent_task)
    of AgentsBroker.call_agent_task instead.

    Works asynchronously.

    :param json_params: Dict in form {
         "coordinates_of_points": List [
            Dict [
                "latitude": float,
                "longitude": float
            ]
        ],
        "categories_names": List[str],
        "user_login": str,
        "amount_of_recommendations_for_point": int,
        "amount_of_additional_recommendations_for_point": int,
        "maximum_amount_of_recommendations": int,
        "maximum_amount_of_additional_recommendations": int,
        "optional_limit": int | None,
    }, where current_name is the name of given landmark
    :return: Coroutine
        List[
            {
                recommendation: Dict | None
            }
        ]
    """
    return await RECOMMENDATIONS_AGENT.find_recommendations_for_coordinates_and_categories(json_params)


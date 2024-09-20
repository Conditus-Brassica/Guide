# Author: Vodohleb04
"""Tasks to work with recommendations agent. Use broker to run tasks"""
from typing import Dict, List
from ..broker_initializer import BROKER
from backend.agents.recommendations_agent.recommendations_agent_initializer import RECOMMENDATIONS_AGENT


@BROKER.task
async def find_recommendations_for_coordinates_task(json_params: Dict):
    """
    Task to get the recommendations (landmarks) that located nearby the given coordinates.

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
        "maximum_amount_of_recommendations": int
    }, where current_name is the name of given landmark
    :return: Coroutine
        List[
            {
                recommendation: Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float,
                    "row_index": int,
                    "row_uuid": string
                ]
            }
        ] or empty List
    """
    return await RECOMMENDATIONS_AGENT.find_recommendations_by_coordinates(json_params)


@BROKER.task
async def post_result_of_recommendations(
        json_params
    ):
        """
        Method to post result of recommendations.
        :json_params["primary_recommendations"] - landmarks, given by the recommendations agent + row_index + row_uuid
        :json_params["result_recommendations"] - landmarks, that were included in the result route (index and uuid are not required)
        :json_params["new_watch_state"] - new watch state of user
        :json_params["new_visit_state"] - new visit state of user
        :json_params["user_reward"] - reward of the recommendations, given by the user (number from range [0, 5])

        ###
        1. json_params: Dict[
            "primary_recommendations": Dict [
                "name": str,
                "latitude": float,
                "longitude": float,
                "row_index": int,
                "row_uuid": string
            ],
            "result_recommendations": Dict [
                "name": str,
                "latitude": float,
                "longitude": float
            ],
            "new_watch_state": List[float],
            "new_visit_state": List[float],
            "user_reward": float | int 
        ]
        """
        return await RECOMMENDATIONS_AGENT.post_result_of_recommendations(json_params)


@BROKER.task
async def count_new_watch_state(json_params) -> List[float]:
    """
    Counts new watch state using old state. 
    s(n + 1) = s(n) * disc_fact + new_watched_landmark

    ###
    1. json_params: Dict[
        "new_watched_landmarks": List[
            Dict[
                "name": str,
                "latitude": float,
                "longitude": float
            ]
        ] 
        "watch_state": List[float]
    ]   

    new_watched_landmarks - landmarks, that causes changing of the state (the most left is the most old watched from the new watched)
        
    watch_state - List of float, old state 
                
    returns: List[float] - new state
    """
    return await RECOMMENDATIONS_AGENT.count_new_watch_state(json_params)
        

@BROKER.task   
async def count_new_visit_state(json_params: Dict) -> List[float]:
    """
    Counts new visit state using old state. 
    s(n + 1) = s(n) * disc_fact + new_visited_landmark

    ###
    1. json_params: Dict[
        "new_visited_landmarks": List[
            Dict[
                "name": str,
                "latitude": float,
                "longitude": float
            ]
        ] 
        "visit_state": List[float]
    ]   

    new_visited_landmarks - landmarks, that causes changing of the state (the most left is the most old visited from the new visited)
        
    visit_state - List of float, old state 
                
    returns: List[float] - new state
    """
    return await RECOMMENDATIONS_AGENT.count_new_visit_state(json_params)


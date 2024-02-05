from typing import List
from backend.broker.broker_initializer import BROKER
from backend.agents.routing_agent.routing_agent_initializer import ROUTING_AGENT


@BROKER.task
async def get_optimized_route_task(landmark_list: dict):
    """
    Method finds all optimized route points for provided points.
    :param landmark_list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
    :return: route points list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
    """
    return await ROUTING_AGENT.get_optimized_route(landmark_list)


@BROKER.task
async def get_optimized_route_main_points_task(landmark_list: dict):
    """
    Method finds all optimized route points for provided points.
    Return one point per 30 km.
    :param landmark_list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
    :return: route points list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
    """
    return await ROUTING_AGENT.get_optimized_route_main_points(landmark_list)

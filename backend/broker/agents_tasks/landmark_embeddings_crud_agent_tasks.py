# Author: Vodohleb04
"""
Tasks to work with embeddings crud agent
"""

from typing import Dict
from backend.broker.broker_initializer import BROKER
from backend.agents.landmark_embeddings_crud.landmark_embeddings_crud_initializer import EMBEDDINGS_CRUD_AGENT

# Read tasks
@BROKER.task
async def get_landmarks_embeddings_task(json_params: Dict):
    """
    Task to get the embeddings of the given landmarks. Do NOT call this task directly. Give it as the first argument (agent_task)
    of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s
    ###
    1. json_params: Dict[
        "landmarks": List[
            Dict[
                "name": str,
                "latitude": float,
                "longitude": float
            ]
        ]
    ]
    returns: Coroutine List[List[float]]
    """
    return await EMBEDDINGS_CRUD_AGENT.get_landmarks_embeddings(json_params)
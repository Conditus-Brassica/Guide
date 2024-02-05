# Author: Meteorych
"""Tasks to work with agent to get landmarks in sectors. Use broker to run tasks"""
from typing import Dict
from ..broker_initializer import BROKER
from backend.agents.landmarks_by_sectors_agent.landmarks_by_sectors_agent_initializer import LANDMARKS_BY_SECTORS_AGENT


@BROKER.task
async def get_landmarks_in_sector_task(json_params: Dict):
    """
        :param json_params: Dict in form {
        "TL": {
            "latitude": double,
            "longitude": double
        },
        "BR": {
            "latitude": double,
            "longitude": double
        }
      }
      :return: LandmarksInMapSectorsCommand for CRUD
    """
    return await LANDMARKS_BY_SECTORS_AGENT.get_landmarks_in_sector(json_params)


@BROKER.task
async def get_landmarks_by_categories_in_sector_task(json_params: Dict):
    """
    #TODO: add categories
    Kick this task to get landmarks, located in passed map sectors. Finds map sectors by their names.
       :param json_params: Dict in form {
        "TL": {
            "latitude": double,
            "longitude": double
        },
        "BR": {
            "latitude": double,
            "longitude": double
        }
      }
    """
    return await LANDMARKS_BY_SECTORS_AGENT.get_landmarks_by_categories_in_sector(json_params)

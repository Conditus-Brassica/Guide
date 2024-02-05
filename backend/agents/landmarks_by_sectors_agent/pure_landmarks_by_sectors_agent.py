from abc import ABC, abstractmethod
from typing import Dict


class PURELandmarksBySectorsAgent(ABC):
    """
        Pure abstract class of Recommendations agent. Provides methods for commands from the other agents.
        All work with kb provided by child classes of this class.

        All methods work asynchronously.
        """

    _single_landmarks_agent = None

    @classmethod
    @abstractmethod
    def get_landmarks_by_sectors_agent(cls):
        """
        Method to take landmarks by sectors agent object. Returns None in case when landmarks by sectors agent is not exists.
        :return: None | PURELandmarksBySectorsAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def landmarks_by_sectors_agent_exists(cls) -> bool:
        """Method to check if landmarks by sectors agent object already exists"""
        raise NotImplementedError

    @abstractmethod
    async def get_landmarks_in_sector(self, json_params: Dict):
        """
        Method to return landmarks in defined sector using PURELandmarksBySectorsAgent
        """
        """
        param json_params: Dict in form {
         "TL": {
             "latitude": Double,
             "longitude": Double
         },
         "BR": {
             "latitude": Double,
             "longitude": Double
         }
        """
        raise NotImplementedError

    @abstractmethod
    async def get_landmarks_by_categories_in_sector(self, json_params: Dict):
        """
        Method to return landmarks of certain categories in defined sector using PURELandmarksBySectorsAgent
        """
        """
        :param json_params: Dict in form {
         "TL": {
             "latitude": Double,
             "longitude": Double
         },
         "BR": {
             "latitude": Double,
             "longitude": Double
         },
         "categories_names": [
            String
        ]
       }
        """
        raise NotImplementedError


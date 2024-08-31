#Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict


class PureRecommendationsAgent(ABC):
    """
    Pure abstract class of Recommendations agent. Provides methods for commands from the other agents.
    All work with kb provided by child classes of this class.

    All methods work asynchronously.
    """

    @classmethod
    @abstractmethod
    def get_recommendations_agent(cls):
        """
        Method to take recommendations agent object. Returns None in case when recommendations agent is not exists.
        :return: None | PureRecommendationsAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def recommendations_agent_exists(cls) -> bool:
        """Method to check if recommendations agent object already exists"""
        raise NotImplementedError

    @abstractmethod
    async def find_recommendations_by_coordinates(self, json_params: Dict):
        """
        Method to get recommendations from agent.

        :param json_params: Dict in form {
             "coordinates_of_points": List [
                Dict [
                    "latitude": float,
                    "longitude": float
                ]
            ],
            "maximum_amount_of_recommendations": int
        },
        :return: Coroutine
            List[
                {
                    recommendation: Dict | None
                }
            ] | None
        """
        raise NotImplementedError

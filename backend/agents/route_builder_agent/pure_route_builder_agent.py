from abc import ABC, abstractmethod
from typing import Dict


class PureRouteBuilder(ABC):
    """
    Class for creating complete route.
    """

    @classmethod
    @abstractmethod
    def get_route_builder_agent(cls):
        """
        Method to take route builder agent object. Returns None in case when route generating agent is not exists.
        :return: None | PureRoutingAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def route_builder_agent_exists(cls) -> bool:
        """
        Method to check if route builder agent exists.
        :return: Boolean
        """
        raise NotImplementedError

    @abstractmethod
    async def build_route(self, route_params: Dict):
        """
        Get completed route.
        :param route_params:  {
            "categories":["category1","category2",...],
            "coordinates":[{"latitude": float, "longitude": float},{"latitude": float, "longitude": float}],
            "user_login": string
        }
        """
        raise NotImplementedError

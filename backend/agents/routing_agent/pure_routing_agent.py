from abc import ABC, abstractmethod


class PureRoutingAgent(ABC):
    """
    Agent for finding route points.
    Usage: when you need to create optimized
    route between several points.
    Uses api_key in api_key.py
    """

    @classmethod
    @abstractmethod
    def get_routing_agent(cls):
        """
        Method to take route generating agent object. Returns None in case when route generating agent is not exists.
        :return: None | PureRoutingAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def routing_agent_exists(cls) -> bool:
        """
        Method to check if route generating agent exists.
        :return: Boolean
        """
        raise NotImplementedError

    @abstractmethod
    async def get_optimized_route(self, landmark_list: list):
        """
        Method finds all optimized route points for provided points.
        :param landmark_list: [[latitude: float, longitude: float], ...]
        :return: Route points, landmarks in route order
        """
        raise NotImplementedError

    @abstractmethod
    async def _create_optimized_route(self):
        """
        Interaction with OpenRoutService API
        :return:
        """
        raise NotImplementedError

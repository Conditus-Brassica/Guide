#Author: Vodohleb04
from backend.broker.abstract_agents_broker import AbstractAgentsBroker

class AgentsBroker(AbstractAgentsBroker):
    """
    Custom broker class to work with agents.
    Class is singleton.
    """
    _single_broker = None

    @classmethod
    def get_broker(cls):
        """
        Method to take broker object. Returns None in case when broker is not exists.
        :return: None | AgentsBroker
        """
        return cls._single_broker

    @classmethod
    def broker_exists(cls) -> bool:
        """Method to check if broker object already exists"""
        if cls._single_broker:
            return True
        else:
            return False

    def __init__(self, *args, **kwargs):
        """
        Init method
        """
        if not self._single_broker:
            super().__init__(*args, **kwargs)
            AgentsBroker._single_broker = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")


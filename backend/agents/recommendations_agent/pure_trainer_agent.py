# Author: Vodohleb04
from abc import ABC, abstractmethod


class PureTrainerAgent(ABC):
    """
    Pure abstract class of Trainer agent. Provides methods for commands from the other agents.

    All methods work asynchronously.
    """

    @classmethod
    @abstractmethod
    def get_trainer_agent(cls):
        """
        Method to take trainer agent object. Returns None in case when trainer agent is not exists.
        :return: None | PureRecommendationsAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def trainer_agent_exists(cls) -> bool:
        """Method to check if trainer agent object already exists"""
        raise NotImplementedError


    async def get_actor_model(self):
        raise NotImplementedError
    
    async def set_actor_model(self, json_params):
        raise NotImplementedError

    async def get_critic_model(self):
        raise NotImplementedError
    
    
    async def set_critic_model(self, json_params):
        raise NotImplementedError

    
    async def get_tau(self):
        raise NotImplementedError
    
    
    async def set_tau(self, json_params):
        raise NotImplementedError

    async def partial_record(self, json_params):
        raise NotImplementedError
    
    async def fill_up_partial_record(self, json_params):
        raise NotImplementedError 

    async def fill_up_partial_record_no_index(self, json_params):
        raise NotImplementedError
        
    async def record(self, json_params):
        raise NotImplementedError

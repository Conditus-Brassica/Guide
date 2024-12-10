# Author: Vodohleb04
from abc import ABC, abstractmethod


class PureNoteTrainerAgent(ABC):
    """
    Pure abstract class of Trainer agent. Provides methods for commands from the other agents.

    All methods work asynchronously.
    """

    @classmethod
    @abstractmethod
    def get_trainer_agent(cls):
        """
        Method to take note_trainer agent object. Returns None in case when note_trainer agent is not exists.
        :return: None | PureNoteTrainerAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def trainer_agent_exists(cls) -> bool:
        """Method to check if note_trainer agent object already exists"""
        raise NotImplementedError

    @abstractmethod
    async def get_actor_model_config(self):
        """
        :returns: Dict[
            "actor_model_config": str
        ]
        """
        raise NotImplementedError

    @abstractmethod
    async def get_actor_model(self):
        """
        :returns: Dict[
            "actor_model": List of weights
        ]
        """
        raise NotImplementedError

    @abstractmethod
    async def get_critic_model_config(self):
        """
        :returns: Dict[
            "critic_model_config": str
        ]
        """
        raise NotImplementedError

    @abstractmethod
    async def get_critic_model(self):
        """
        :returns: Dict[
            "critic_model": List of weights
        ]
        """
        raise NotImplementedError

    @abstractmethod
    async def partial_record_with_next_state(self, json_params):
        """
        Is used to write state, action and next_state of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: List[float]
        2. action: List[float]
        3. next_state: List[float]

        returns: Tuple[int, uuid.hex] - index of row in buffer and hex of uuid of the row.
        """
        raise NotImplementedError

    # @abstractmethod
    # async def partial_record_list_with_next_state(self, json_params):
    #     """
    #     Is used to write lists of state, action and next_state of sars tuple. This tuple will be saved, but won't be used in training samples
    #
    #     ###
    #     1. state_list: List[List[float]]
    #     2. action_list: List[List[float]]
    #     3. next_state_list: List[List[float]]
    #
    #     returns: Tuple[int, uuid.hex] - index of row in buffer and hex of uuid of the row.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # async def fill_up_partial_record_reward_only(self, json_params):
    #     """
    #     Is used to write the reward of sars tuple. If the given hex of uuid was found in buffer, reward will be saved
    #         and the row may be used in training batch.
    #
    #     1. row_index: int
    #         - index of the row in buffer (such index is returned as result of partial_record method)
    #     2. row_uuid: uuid.hex
    #         - hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
    #     3. reward: float
    #
    #     returns: bool - True if hex of uuid is correct, False otherwise
    #     """
    #     raise NotImplementedError

    @abstractmethod
    async def fill_up_partial_record_reward_only_list(self, json_params):
        """
        Is used to write the reward of sars tuple. If the given hex of uuid was found in buffer, reward will be saved
            and the row may be used in training batch.

        1. row_index_list: List[int]
            - index of the row in buffer (such index is returned as result of partial_record method)
        2. row_uuid_list: List[uuid.hex]
            - hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
        3. reward_list: List[float]

        returns: List[bool] - True if hex of uuid is correct, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    async def train(self, json_params):
        """
        Start training process if there is any completed record in the sars buffer

        :repeat_amount: int > 0 - amount of repeats of training

        :returns: Dict[
            "actor_model": List of weights,
            "critic_model": List of weights
        ]
        """
        raise NotImplementedError

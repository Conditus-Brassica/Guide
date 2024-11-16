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
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def trainer_agent_exists(cls) -> bool:
        """Method to check if note_trainer agent object already exists"""
        raise NotImplementedError


    async def get_actor_model_config(self):
        raise NotImplementedError
    

    async def get_actor_model(self):
        raise NotImplementedError

    
    async def set_actor_model(self, json_params):
        raise NotImplementedError


    async def get_critic_model_config(self):
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
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: List[float]
        2. action: List[float]

        returns: Tuple[int, uuid.hex] - index of row in buffer and hex of uuid of the row.
        """
        raise NotImplementedError
    
    
    async def partial_record_list(self, json_params):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples
        Common state for multiple actions

        ###
        1. state: List[float]
        2. action_list: List[List[float]]

        returns: Tuple[List[int], List[uuid.hex]] - indices of rows in buffer and hex of uuids of the rows in buffer.
        """
        raise NotImplementedError
    
    
    async def fill_up_partial_record(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid_list: uuid.hex
            - hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
        3. reward: float
        4. next_state: List[float]

        returns: bool - True if hex of uuid is correct, False otherwise
        """
        raise NotImplementedError
    
    
    async def fill_up_partial_record_list(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: List[int]
            - indices of the rows in buffer (such indices are returned as result of partial_record method) 
        2. row_uuid_list: List[uuid.hex]
            - hex of uuids of the rows in buffer (such hex of uuids are returned as result of partial_record method)
        3. reward_list: List[float]
        4. next_state: List[float]

        returns: List[bool] - True if hex of uuid is correct, False otherwise
        """
        raise NotImplementedError
    

    async def fill_up_partial_record_no_index(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out hex of uuid.

        1. row_uuid: uuid.hex
            - hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
        2. reward: float
        3. next_state: List[float]

        returns: bool - True if hex of uuid was found out, False otherwise
        """
        raise NotImplementedError
    

    async def fill_up_partial_record_list_no_index(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out hex of uuid.

        1. row_uuid_list: List[uuid.hex]
            - hex of uuids of the rows in buffer (such hex of uuids are returned as result of partial_record method)
        2. reward_list: List[float]
        3. next_state: List[float]

        returns: List[bool] - True if hex of uuid was found out, False otherwise
        """
        raise NotImplementedError
    

    async def record(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple: Tuple[List[float], List[float], float, List[float]]

        :returns: Tuple[int, uuid.hex] - row index, hex of uuid of the row
        """
        raise NotImplementedError
    

    async def record_list(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple_list: List[Tuple[List[float], List[float], float, List[float]]]

        :returns: Tuple[List[int], List[uuid.hex]] - row index, hex of uuid of the row
        """
        raise NotImplementedError


    async def train(self, json_params):
        """
        Start training process if there is any completed record in the sars buffer

        :repeat_amount: int > 0 - amount of repeats of training
        """
        raise NotImplementedError
    

    async def get_state(self, json_params):
        """
        Returns state of the sars tuple if the given hex of uuid is correct

        :row_index: int
        :row_uuid: uuid.hex

        :returns: List[float] | None
        """
        raise NotImplementedError
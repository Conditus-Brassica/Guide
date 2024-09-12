# Author: Vodohleb04
from backend.agents.recommendations_agent.pure_trainer_agent import PureTrainerAgent
from backend.agents.recommendations_agent.trainer import Trainer


class TrainerAgent(PureTrainerAgent):
    _single_trainer = None
    _trainer: Trainer = None

    @classmethod
    def get_trainer_agent(cls):
        return cls._single_trainer

    @classmethod
    def trainer_agent_exists(cls) -> bool:
        """Method to check if trainer object already exists"""
        if cls._single_trainer:
            return True
        else:
            return False

    @classmethod
    def _class_init(
            cls, trainer: Trainer
    ):
        cls._trainer = trainer

    def __init__(self, trainer: Trainer):
        if not self._single_trainer:
            self._class_init(trainer)
            self._single_trainer = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")
        
    
    async def get_actor_model(self):
        return {"actor_model": self._trainer.actor_model}
    
    
    async def set_actor_model(self, json_params):
        self._trainer.actor_model = json_params["actor_model"]

    
    async def get_critic_model(self):
        return {"critic_model": self._trainer.critic_model}
    
    
    async def set_critic_model(self, json_params):
        self._trainer.critic_model = json_params["actor_model"]

    
    async def get_tau(self):
        return {"tau": self._trainer.tau}
    
    
    async def set_tau(self, json_params):
        self._trainer.tau = json_params["tau"]

    async def partial_record(self, json_params):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: numpy.ndarray
        2. action: numpy.ndarray

        returns: Tuple[int, uuid] - index of row in buffer and uuid of row.
        """
        
        return await self._trainer.partial_record(json_params["state"], json_params["action"])
    
    async def partial_record_list(self, json_params):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples
        Common state for multiple actions

        ###
        1. state: numpy.ndarray
        2. action_list: List[numpy.ndarray]

        returns: Tuple[List[int], List[uuid]] - indices of rows in buffer and uuids of rows in buffer.
        """
        return await self._trainer.partial_record_list(json_params["state"], json_params["action_list"])
    
    async def fill_up_partial_record(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid_list: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        3. reward: numpy.ndarray
        4. next_state: numpy.ndarray

        returns: bool - True if uuid is correct, False otherwise
        """
        return await self._trainer.fill_up_partial_record(
            json_params["row_index"], json_params["row_uuid"], json_params["reward"], json_params["next_state"]
        )
    
    async def fill_up_partial_record_list(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: List[int]
            - indices of the rows in buffer (such indices are returned as result of partial_record method) 
        2. row_uuid_list: List[uuid]
            - uuids of the rows in buffer (such uuids are returned as result of partial_record method)
        3. reward_list: List[numpy.ndarray]
        4. next_state: numpy.ndarray

        returns: List[bool] - True if uuid is correct, False otherwise
        """
        return await self._trainer.fill_up_partial_record_list(
            json_params["row_index_list"], json_params["row_uuid_list"], json_params["reward_list"], json_params["next_state"]
        )  

    async def fill_up_partial_record_no_index(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out uuid.

        1. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        2. reward: numpy.ndarray
        3. next_state: numpy.ndarray

        returns: bool - True if uuid was found out, False otherwise
        """
        return await self._trainer.fill_up_partial_record_no_index(
            json_params["row_uuid"], json_params["reward"], json_params["next_state"]
        )
    

    async def fill_up_partial_record_list_no_index(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out uuid.

        1. row_uuid_list: List[uuid]
            - uuids of the rows in buffer (such uuids are returned as result of partial_record method)
        2. reward_list: numpy.ndarray
        3. next_state: numpy.ndarray

        returns: List[bool] - True if uuid was found out, False otherwise
        """
        return await self._trainer.fill_up_partial_record_list_no_index(
            json_params["row_uuid_list"], json_params["reward_list"], json_params["next_state"]
        )
        

    async def record(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]

        :returns: Tuple[int, uuid] - row index, row uuid
        """
        return await self._trainer.record(json_params["sars_tuple"])
    

    async def record_list(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple_list: List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]

        :returns: Tuple[List[int], List[uuid]] - row index, row uuid
        """
        return await self._trainer.record_list(json_params["sars_tuple_list"])


    async def train(self, json_params):
        """
        Start training process if there is any completed record in the sars buffer

        :repeat_amount: int > 0 - amount of repeats of training
        """
        return await self._trainer.train(json_params["repeat_amount"])
    

    async def get_state(self, json_params):
        """
        Returns state of the sars tuple if the given uuid is correct

        :row_index: int
        :row_uuid: uuid4

        :returns: numpy.ndarray | None
        """
        return await self._trainer.get_state(json_params["row_index"], json_params["row_uuid"])

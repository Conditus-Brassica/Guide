# Author: Vodohleb04
from backend.agents.recommendations_agent.pure_trainer_agent import PureTrainerAgent
from backend.agents.recommendations_agent.trainer import Trainer


class TrainerAgent(PureTrainerAgent):
    _single_trainer = None
    _trainer = None

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
        return {"tau": self._tau}
    
    
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
        
        return self._trainer.partial_record(json_params["state"], json_params["action"])
    
    async def fill_up_partial_record(self, json_params):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        3. reward: numpy.ndarray
        4. next_state: numpy.ndarray

        returns: bool - True if uuid is correct, False otherwise
        """
        return self._trainer.fill_up_partial_record(
            json_params["row_index"], json_params["row_uuid"], json_params["reward"], json_params["next_state"]
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
        return self._trainer.fill_up_partial_record_no_index(json_params["row_uuid"], json_params["reward"], json_params["next_state"])
        
    async def record(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        return self._trainer.record(json_params["sars_tuple"])
    
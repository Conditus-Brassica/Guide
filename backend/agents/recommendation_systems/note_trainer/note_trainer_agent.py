# Author: Vodohleb04
import numpy as np
from backend.agents.recommendation_systems.note_trainer.pure_note_trainer_agent import PureNoteTrainerAgent
from backend.agents.recommendation_systems.note_trainer.note_trainer import NoteTrainer


class NoteTrainerAgent(PureNoteTrainerAgent):
    _single_trainer = None
    _trainer: NoteTrainer = None

    @classmethod
    def get_trainer_agent(cls):
        return cls._single_trainer

    @classmethod
    def trainer_agent_exists(cls) -> bool:
        """Method to check if landmark_trainer object already exists"""
        if cls._single_trainer:
            return True
        else:
            return False

    @classmethod
    def _class_init(cls, trainer: NoteTrainer):
        cls._trainer = trainer

    def __init__(self, trainer: NoteTrainer):
        
        if not self._single_trainer:
            self._class_init(trainer)
            self._single_trainer = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")
        
    
    async def get_actor_model_config(self):
        return {"actor_model_config": self._trainer.get_actor_model_config()}
    

    async def get_actor_model(self):
        return {
            "actor_model": [
                weight.tolist() for weight in self._trainer.actor_model.get_weights()
            ]
        }

    
    async def set_actor_model(self, json_params):
        self._trainer.actor_model = json_params["actor_model"]


    async def get_critic_model_config(self):
        return {"critic_model_config": self._trainer.get_critic_model_config()}

    
    async def get_critic_model(self):
        return {
            "critic_model": [
                weight.tolist() for weight in self._trainer.critic_model.get_weights()
            ]
        }
    
    
    async def set_critic_model(self, json_params):
        self._trainer.critic_model = json_params["actor_model"]

    
    async def get_tau(self):
        return {"tau": self._trainer.tau}
    
    
    async def set_tau(self, json_params):
        self._trainer.tau = json_params["tau"]


    async def partial_record_with_next_state(self, json_params):
        return self._trainer.partial_record_with_next_state(
            np.asarray(json_params["state"], dtype=self._trainer.np_dtype),
            np.asarray(json_params["action"], dtype=self._trainer.np_dtype),
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )


    async def partial_record_list_with_next_state(self, json_params):
        return self._trainer.partial_record_list_with_next_state(
            np.asarray(json_params["state"], dtype=self._trainer.np_dtype),
            [
                np.asarray(json_params["action_list"][i], dtype=self._trainer.np_dtype)
                for i in range(len(json_params["action_list"]))
            ],
            [
                np.asarray(json_params["next_state_list"][i], dtype=self._trainer.np_dtype)
                for i in range(len(json_params["next_state_list"]))
            ]
        )


    async def fill_up_partial_record_reward_only(self, json_params):
        return self._trainer.fill_up_partial_record_reward_only(
            json_params["row_index"],
            json_params["row_uuid"],
            self._trainer.np_dtype(json_params["reward"])
        )


    async def fill_up_partial_record_reward_only_list(self, json_params):
       return self._trainer.fill_up_partial_record_reward_only_list(
           json_params["row_index_list"],
           json_params["row_uuid_list"],
           [
               self._trainer.np_dtype(json_params["reward_list"][i])
               for i in range(len(json_params["reward_list"]))
           ],
       )


    async def train(self, json_params):
        await self._trainer.train(json_params["repeat_amount"])

        return {
            "actor_model": [
                weight.tolist() for weight in self._trainer.actor_model.get_weights()
            ],
            "critic_model": [
                weight.tolist() for weight in self._trainer.critic_model.get_weights()
            ]
        }

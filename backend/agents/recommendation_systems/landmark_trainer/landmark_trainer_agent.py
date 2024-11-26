# Author: Vodohleb04
import numpy as np
from backend.agents.recommendation_systems.landmark_trainer.pure_landmark_trainer_agent import PureLandmarkTrainerAgent
from backend.agents.recommendation_systems.landmark_trainer.landmark_trainer import LandmarkTrainer


class LandmarkTrainerAgent(PureLandmarkTrainerAgent):
    _single_trainer = None
    _trainer: LandmarkTrainer = None

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
    def _class_init(cls, trainer: LandmarkTrainer):
        cls._trainer = trainer

    def __init__(self, trainer: LandmarkTrainer):
        
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


    async def partial_record(self, json_params):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: List[float]
        2. action: List[float]

        returns: Tuple[int, uuid.hex] - index of row in buffer and hex of uuid of the row.
        """
        
        return self._trainer.partial_record(
            np.asarray(json_params["state"], dtype=self._trainer.np_dtype),
            np.asarray(json_params["action"], dtype=self._trainer.np_dtype)
        )


    async def partial_record_list(self, json_params):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples
        Common state for multiple actions

        ###
        1. state: List[float]
        2. action_list: List[List[float]]

        returns: Tuple[List[int], List[uuid.hex]] - indices of rows in buffer and hex of uuids of the rows in buffer.
        """
        return self._trainer.partial_record_list(
            np.asarray(json_params["state"], dtype=self._trainer.np_dtype), 
            [
                np.asarray(json_params["action_list"][i], dtype=self._trainer.np_dtype)
                for i in range(len(json_params["action_list"]))
            ]
        )


    async def fill_up_partial_record(self, json_params):
        return self._trainer.fill_up_partial_record(
            json_params["row_index"],
            json_params["row_uuid"],
            self._trainer.np_dtype(json_params["reward"]),
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )


    async def fill_up_partial_record_list(self, json_params):
        return self._trainer.fill_up_partial_record_list(
            json_params["row_index_list"],
            json_params["row_uuid_list"],
            [
                self._trainer.np_dtype(json_params["reward_list"][i])
                for i in range(len(json_params["reward_list"]))
            ],
            [
                np.asarray(json_params["next_state_list"][i], dtype=self._trainer.np_dtype)
                for i in range(len(json_params["next_state_list"]))
            ]
        )


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


    async def fill_up_partial_record_reward_only_replace_next_state(self, json_params):
        return self._trainer.fill_up_partial_record_reward_only_replace_next_state(
            json_params["row_index"],
            json_params["row_uuid"],
            self._trainer.np_dtype(json_params["reward"])
        )


    async def fill_up_partial_record_reward_only_replace_next_state_list(self, json_params):
       return self._trainer.fill_up_partial_record_reward_only_replace_next_state_list(
           json_params["row_index_list"],
           json_params["row_uuid_list"],
           [
               self._trainer.np_dtype(json_params["reward_list"][i])
               for i in range(len(json_params["reward_list"]))
           ],
       )


    async def record(self, json_params):
        return self._trainer.record(
            (
                np.asarray(json_params["sars_tuple"][0], dtype=self._trainer.np_dtype),
                np.asarray(json_params["sars_tuple"][1], dtype=self._trainer.np_dtype),
                self._trainer.np_dtype(json_params["sars_tuple"][2]),
                np.asarray(json_params["sars_tuple"][3], dtype=self._trainer.np_dtype),
            )
        )
    

    async def record_list(self, json_params):
        return self._trainer.record_list(
            [
                (
                    np.asarray(json_params["sars_tuple_list"][i][0], dtype=self._trainer.np_dtype),
                    np.asarray(json_params["sars_tuple_list"][i][1], dtype=self._trainer.np_dtype),
                    self._trainer.np_dtype(json_params["sars_tuple_list"][i][2]),
                    np.asarray(json_params["sars_tuple_list"][i][3], dtype=self._trainer.np_dtype),
                )
                for i in range(len(json_params["sars_tuple_list"]))
            ]
        )


    async def remove_record(self, json_params):
        return {"result": self._trainer.remove_record(json_params["row_index"], json_params["row_uuid"])}


    async def remove_record_list(self, json_params):
        return {
            "result": self._trainer.remove_record_list(json_params["row_index_list"], json_params["row_uuid_list"])
        }


    async def train(self, json_params):
        self._trainer.train(json_params["repeat_amount"])

        return {
            "actor_model": [
                weight.tolist() for weight in self._trainer.actor_model.get_weights()
            ],
            "critic_model": [
                weight.tolist() for weight in self._trainer.critic_model.get_weights()
            ]
        }
    

    async def get_state(self, json_params):
        state = self._trainer.get_state(json_params["row_index"], json_params["row_uuid"])
        if state is not None:
            return state.tolist()
        else:
            return state    
        
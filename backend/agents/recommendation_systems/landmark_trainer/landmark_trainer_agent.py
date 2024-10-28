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
    def _class_init(
            cls, trainer: LandmarkTrainer
    ):
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
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid_list: uuid.hex
            -hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
        3. reward: float
        4. next_state: List[float]

        returns: bool - True if hex of uuid is correct, False otherwise
        """
        return self._trainer.fill_up_partial_record(
            json_params["row_index"],
            json_params["row_uuid"],
            self._trainer.np_dtype(json_params["reward"]),
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )
    
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
        return self._trainer.fill_up_partial_record_list(
            json_params["row_index_list"],
            json_params["row_uuid_list"],
            [
                self._trainer.np_dtype(json_params["reward_list"][i])
                for i in range(len(json_params["reward_list"]))
            ],
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )  

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
        return self._trainer.fill_up_partial_record_no_index(
            json_params["row_uuid"],
            self._trainer.np_dtype(json_params["reward"]),
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )
    

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
        return self._trainer.fill_up_partial_record_list_no_index(
            json_params["row_uuid_list"],
            [
                self._trainer.np_dtype(json_params["reward_list"][i])
                for i in range(len(json_params["reward_list"]))
            ],
            np.asarray(json_params["next_state"], dtype=self._trainer.np_dtype)
        )
        

    async def record(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple: Tuple[List[float], List[float], float, List[float]]

        :returns: Tuple[int, uuid.hex] - row index, hex of uuid of the row
        """
        return self._trainer.record(
            (
                np.asarray(json_params["sars_tuple"][0], dtype=self._trainer.np_dtype),
                np.asarray(json_params["sars_tuple"][1], dtype=self._trainer.np_dtype),
                self._trainer.np_dtype(json_params["sars_tuple"][2]),
                np.asarray(json_params["sars_tuple"][3], dtype=self._trainer.np_dtype),
            )
        )
    

    async def record_list(self, json_params):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        sars_tuple_list: List[Tuple[List[float], List[float], float, List[float]]]

        :returns: Tuple[List[int], List[uuid.hex]] - row index, hex of uuid of the row
        """
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


    def remove_record(self, json_params):
        """
        Removes record from SARS buffer

        :param json_params: - Dict[
            "row_index": int,
            "row_uuid": uuid4.hex
        ]

        :returns: {"result": bool}, True if record was successfully removed
        """
        return {"result": self._trainer.remove_record(json_params["row_index"], json_params["row_uuid"])}


    def remove_record_list(self, json_params):
        """
            Removes records from SARS buffer

            :param json_params: - Dict[
                "row_index_list": List[int],
                "row_uuid_list": List[uuid4.hex]
            ]

            :returns: {"result": List[bool]}, True if record was successfully removed
        """
        return {
            "result": self._trainer.remove_record_list(json_params["row_index_list"], json_params["row_uuid_list"])
        }


    def remove_record_no_index(self, json_params):
        """
            Removes record from SARS buffer

            :param json_params: - Dict["row_uuid": uuid4.hex]

            :returns: {"result": bool}, True if record was successfully removed
        """
        return {"result": self._trainer.remove_record_no_index(json_params["row_uuid"])}


    def remove_record_list_no_index(self, json_params):
        """
            Removes records from SARS buffer

            :param json_params: - Dict["row_uuid_list": List[uuid4.hex] ]

            :returns: {"result": List[bool]}, True if record was successfully removed
        """
        return {"result": self._trainer.remove_record_list_no_index(json_params["row_uuid_list"])}


    async def train(self, json_params):
        """
        Start training process if there is any completed record in the sars buffer

        :repeat_amount: int > 0 - amount of repeats of training
        """

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
        """
        Returns state of the sars tuple if the given hex of uuid is correct

        :row_index: int
        :row_uuid: uuid.hex

        :returns: List[float] | None
        """
        state = self._trainer.get_state(json_params["row_index"], json_params["row_uuid"])
        if state is not None:
            return state.tolist()
        else:
            return state    
        
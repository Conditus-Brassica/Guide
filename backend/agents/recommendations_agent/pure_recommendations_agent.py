#Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict, Tuple
import keras
import numpy as np
import tensorflow as tf


class PureRecommendationsAgent(ABC):
    """
    Pure abstract class of Recommendations agent. Provides methods for commands from the other agents.

    All methods work asynchronously.
    """

    @classmethod
    @abstractmethod
    def get_recommendations_agent(cls):
        """
        Method to take recommendations agent object. Returns None in case when recommendations agent is not exists.
        :return: None | PureRecommendationsAgent
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def recommendations_agent_exists(cls) -> bool:
        """Method to check if recommendations agent object already exists"""
        raise NotImplementedError
      
    @property
    @abstractmethod
    def actor_model(self) -> keras.Model:
        raise NotImplementedError
    

    @actor_model.setter
    @abstractmethod
    async def actor_model(self, actor_model: keras.Model):
        raise NotImplementedError


    @property
    @abstractmethod
    def critic_model(self) -> keras.Model:
        raise NotImplementedError

    
    @critic_model.setter
    async def critic_model(self, critic_model: keras.Model):
        raise NotImplementedError

    
    async def count_new_watch_state(
        self, new_watched_landmark: Dict, watch_state: np.ndarray
    ) -> np.ndarray:
        """
        Counts new watch state using old state. 
        s(n + 1) = s(n) * disc_fact + new_watched_landmark

        ###
        1. new_watched_landmark: Dict["name": str, "latitude": float, "longitude": float]
            - landmark, that causes changing of the state
        2. watch_state: numpy.ndarray
            - float ndarray, old state        
            returns: numpy.ndarray - new state
        """
        raise NotImplementedError
    
    async def count_new_visit_state(
        self, new_visited_landmark: Dict, visit_state: np.ndarray
    ) -> np.ndarray:
        """
        Counts new visit state using old state. 
        s(n + 1) = s(n) * disc_fact + new_visited_landmark

        ###
        1. new_visited_landmark: Dict["name": str, "latitude": float, "longitude": float]
            - landmark, that causes changing of the state
        2. visit_state: numpy.ndarray
            - float ndarray, old state
        
            returns: numpy.ndarray - new state
        """
        raise NotImplementedError
    
    
    async def concat_state(self, base_states: Tuple[np.ndarray], mask: Tuple[float] | None = None, return_tf_tensor=False) -> np.ndarray | tf.Tensor:
        """
        Concatenate the given states in the given order.

        result = base_states[0] * mask[0] \\\/ base_states[1] * mask[1] \\\/ ... \\\/ base_states[n] * mask[n]
        ###
        1. base_states: Tuple[numpy.ndarray]
            - States to concatenate, presented in the numpy.ndarray
        2.* mask: Tuple[float] [DEFAULT] = None
            - Float factors in range [0, 1] to mask the states. 
        3.* return_tf_tensor: bool [DEFAULT = False]
            - Returns tensorflow.Tensor if True, numpy.ndarray otherwise
        """
        raise NotImplementedError


    @abstractmethod
    async def find_recommendations_by_coordinates(self, json_params: Dict):
        """
        Method to get recommendations from agent.

        :param json_params: Dict in form {
             "coordinates_of_points": List [
                Dict [
                    "latitude": float,
                    "longitude": float
                ]
            ],
            "watch_state": List[float],
            "visit_state": List[float],
            "maximum_amount_of_recommendations": int
        },
        :return: Coroutine
            List[
                {
                    "recommendation": Dict,
                    "buffer_index": int,
                    "buffer_uuid": uuid4
                }
            ] | empty list
        """
        raise NotImplementedError


    @abstractmethod
    async def post_result_of_recommendations(
            self, json_params
    ):
        """
        Method to post result of recommendations.
        :json_params["primary_recommendations"] - landmarks, given by the recommendations agent + buffer_index + buffer_uuid
        :json_params["result_recommendations"] - landmarks, that were included in the result route (index and uuid are not required)
        :json_params["new_watch_state"] - new watch state of user
        :json_params["new_visit_state"] - new visit state of user
        :json_params["user_reward"] - reward of the recommendations, given by the user (number from range [0, 5])

        ###
        1. json_params: Dict[
            "primary_recommendations": Dict [
                "name": str,
                "latitude": float,
                "longitude": float,
                "buffer_index": int,
                "buffer_uuid": uuid4
            ],
            "result_recommendations": Dict [
                "name": str,
                "latitude": float,
                "longitude": float
            ],
            "new_watch_state": List[float],
            "new_visit_state": List[float],
            "user_reward": float | int 
        ]
        """
        raise NotImplementedError


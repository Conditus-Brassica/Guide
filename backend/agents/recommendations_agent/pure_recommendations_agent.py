#Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict, List
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
    async def actor_model(self) -> keras.Model:
        raise NotImplementedError
    

    @actor_model.setter
    @abstractmethod
    async def actor_model(self, actor_model: keras.Model):
        raise NotImplementedError


    @property
    @abstractmethod
    async def critic_model(self) -> keras.Model:
        raise NotImplementedError

    
    @critic_model.setter
    async def critic_model(self, critic_model: keras.Model):
        raise NotImplementedError

    
    async def count_new_watch_state(self, json_params: Dict) -> List[float]:
        """
        Counts new watch state using old state. 
        s(n + 1) = s(n) * disc_fact + new_watched_landmark

        ###
        1. json_params: Dict[
            "new_watched_landmarks": List[
                Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float
                ]
            ] 
            "watch_state": List[float]
        ]   

        new_watched_landmarks - landmarks, that causes changing of the state (the most left is the most old watched from the new watched)
            
        watch_state - List of float, old state 
                   
        returns: List[float] - new state
        """
        raise NotImplementedError
    

    async def count_new_visit_state(self, json_params: Dict) -> List[float]:
        """
        Counts new visit state using old state. 
        s(n + 1) = s(n) * disc_fact + new_visited_landmark

        ###
        1. json_params: Dict[
            "new_visited_landmarks": List[
                Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float
                ]
            ] 
            "visit_state": List[float]
        ]   

        new_visited_landmarks - landmarks, that causes changing of the state (the most left is the most old visited from the new visited)
            
        visit_state - List of float, old state 
                   
        returns: List[float] - new state
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
                Dict[
                    "recommendation": Dict[
                        "name": str,
                        "latitude": float,
                        "longitude": float,
                        "row_index": int,
                        "row_uuid": uuid.hex
                    ]
                ]
            ] | empty list
        """
        raise NotImplementedError


    @abstractmethod
    async def post_result_of_recommendations(
            self, json_params
    ):
        """
        Method to post result of recommendations.
        :json_params["primary_recommendations"] - landmarks, given by the recommendations agent + row_index + row_uuid
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
                "row_index": int,
                "row_uuid": uuid.hex
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
    

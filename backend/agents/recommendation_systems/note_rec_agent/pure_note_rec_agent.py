#Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict, List
import keras


class PureNoteRecAgent(ABC):
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


    @abstractmethod
    async def count_new_state(self, json_params: Dict) -> List[float]:
        """
        Counts new state using old state.
        s(n + 1) = s(n) * disc_fact + new_note

        :param json_params: Dict[
            "new_notes": List[
                Dict[
                    "title": str
                ]
            ] 
            "state": List[float]
        ]   

        new_notes - notes, that causes changing of the state (the most left is the most old watched from the new watched)
            
        state - List of float, old state
                   
        returns: List[float] - new state
        """
        raise NotImplementedError


    @abstractmethod
    async def make_recommendations(self, json_params: Dict):
        """
        Method to make recommendations by agent. Method doesn't make partial record for user interaction with note, it
        only returns titles of notes.

        :param json_params: Dict in form {
            "state": List[float],
            "maximum_amount_of_recommendations": int
        },
        :return: Coroutine
            List[
                Dict[
                    "recommendation": Dict["title": str]
                ]
            ] | empty list
        """
        raise NotImplementedError


    @abstractmethod
    async def interaction_with_note_started(self, json_params: Dict):
        """
        Method to give agent information about started interaction with note.

        :param json_params: Dict in form {
            "state": List[float],
            "note_title": str
        }
        :return: Coroutine
            Dict [
                "row_uuid": uuid4.hex,
                "row_index": int
            ]
        """
        raise NotImplementedError



    @abstractmethod
    async def interactions_with_notes_finished(self, json_params):
        """
        Method to end user interactions with notes. This method is used to end interactions. Takes uuid and index of
        partial record for user interaction with note.
        :json_params["interactions"] - list of user interactions with notes

        ###
        :param json_params: Dict[
            "interactions": List[
                Dict [
                    "row_uuid": uuid4.hex,
                    "row_index": int,
                    "user_reaction": Enum.UserReaction,
                    "relative_interaction_time": float
                ]
            ]
        ]

        "relative_interaction_time": float - interaction time relative to expected reading time of note
        """
        raise NotImplementedError
    

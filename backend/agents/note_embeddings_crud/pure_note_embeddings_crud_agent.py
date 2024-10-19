# Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict


class PureNoteEmbeddingsCRUDAgent(ABC):
    """
    Base class for CRUD agent, that provided to manage notes embeddings database.

    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
    """
    
    @classmethod
    @abstractmethod
    def get_embeddings_crud(cls):
        """
        Method to take notes embeddings crud agent object. Returns None in case when crud is not exists.
        :return: None | PureEmbeddingsCRUDAgent
        """
        # return cls._single_crud
        raise NotImplementedError


    @classmethod
    @abstractmethod
    def embeddings_crud_exists(cls) -> bool:
        raise NotImplementedError
    

    @classmethod
    @abstractmethod
    async def get_nearest_notes(cls, json_params: Dict):
        """
        Read query to get embeddings of the notes, nearest to the given one.
        Works asynchronously.

        ###
        1. json_params: Dict[
            "note_embedding": List[float],
            "limit": int,
            "return_embeddings": bool
        ]

        returns: Coroutine
            Dict[
                note_titles: List[str], embeddings: List[List[float]]
            ] |
            Dict[
                note_titles: List[str]
            ]
        """
        raise NotImplementedError

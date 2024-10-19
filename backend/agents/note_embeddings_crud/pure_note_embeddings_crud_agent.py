# Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict, List


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
    

    # Read queries
    @abstractmethod
    async def get_nearest_notes(self, json_params: Dict):
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


    # Write queries
    async def add_note_embedding(self, json_params: Dict):
        """
        Write query to add embedding of the note to the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title": str,
            "note_embedding": List[float]
        ]

        :return: Coroutine Dict{"result": bool}, True, if is successfully added
        """
        raise NotImplementedError


    # Update queries
    async def update_note_embedding(self, json_params: Dict):
        """
        Update query to update embedding of the note, stored in the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title": str,
            "note_embedding": List[float]
        ], where note_embedding is the new embedding of the given note.

        :return: Coroutine Dict["result": bool], True if is successfully updated.
        """
        raise NotImplementedError


    # Delete queries
    async def delete_notes_embeddings(self, json_params: Dict):
        """
        Delete query to remove the given notes from the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title_list": List[str]
        ]

        :return: Coroutine Dict["result": True]
        """
        raise NotImplementedError

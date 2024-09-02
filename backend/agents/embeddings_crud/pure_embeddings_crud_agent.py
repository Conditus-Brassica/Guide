# Author: Vodohleb04
from abc import ABC, abstractmethod


class PureEmbeddingsCRUDAgent(ABC):
    """
    Base class for CRUD agent, that provided to manage embeddings database.

    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
    """
    
    @classmethod
    @abstractmethod
    def get_embeddings_crud(cls):
        """
        Method to take embeddings crud agent object. Returns None in case when crud is not exists.
        :return: None | PureEmbeddingsCRUDAgent
        """
        # return cls._single_crud
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def embeddings_crud_exists(cls) -> bool:
        """Method to check if embeddings crud object already exists"""
        raise NotImplementedError
    

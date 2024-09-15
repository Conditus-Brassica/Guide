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
        """
        Read query to get embeddings of the given landmarks.
        Works asynchronously.

        ###
        1. json_params: Dict[
            "landmarks": List[
                Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float
                ]
            ]
        ]
            - landmarks, for wich the embedding is returned
        returns: Coroutine List[[List[float]] - List of embeddings of the given landmarks
        """
        raise NotImplementedError
    

    @classmethod
    @abstractmethod
    async def get_landmarks_embeddings(cls, json_params: Dict):
        """
        Read query to get embeddings of the given landmarks.
        Works asynchronously.

        ###
        1. json_params: Dict[
            "landmarks": List[
                Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float
                ]
            ]
        ]
            - landmarks, for wich the embedding is returned
        returns: Coroutine List[List[float]]
        """
        raise NotImplementedError

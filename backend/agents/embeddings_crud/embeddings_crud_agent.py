# Author: Vodohleb04
"""
Embeddings CRUD module.
SELECT, INSERT, UPDATE and DELETE queries to embeddings database

https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
"""
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.agents.embeddings_crud.pure_embeddings_crud_agent import PureEmbeddingsCRUDAgent
from backend.agents.embeddings_crud.embeddings_reader import EmbeddingsReader


class EmbeddingsCRUD(PureEmbeddingsCRUDAgent):
    """
    Class to work with embeddings database. Provides read, write, update and delete queries for embeddings database.
    All methods work asynchronously.
    
    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s
    """
    
    _single_embeddings_crud = None
    _db_engine: AsyncEngine = None

    @classmethod
    def get_embeddings_crud(cls):
        return cls._single_embeddings_crud
    
    @classmethod
    def embeddings_crud_exists(cls) -> bool:
        if cls._single_embeddings_crud:
            return True
        else:
            return False

    @classmethod    
    def _class_init(cls, db_engine: AsyncEngine):
        cls._db_engine = db_engine

    def __init__(self, db_engine: AsyncEngine):
        """
        Class to work with embeddings database. Provides read, write, update and delete queries for embeddings database
    
        https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s

        ###
        1. db_engine: sqlalchemy.ext.asyncio.AsyncEngine
            - AsyncEngine, that provides connection to embeddings database
        """
        if not self._single_embeddings_crud:
            self._class_init(db_engine)
            self._single_embeddings_crud = self
        else:
            RuntimeError("Unexpected behaviour, this class can have only one instance")

    # Read queries

    @classmethod
    async def get_landmarks_embeddings(cls, json_params: Dict):
        """
        Read query to get embeddings of the given landmarks.
        Works asynchronously.

        ###
        1. db_connection: sqlalchemy.ext.asyncio.AsyncConnection
            - async connection to the embeddings database
        2. json_params: Dict[
            "landmarks": List[
                Dict[
                    "name": str,
                    "latitude": float,
                    "longitude": float
                ]
            ]
        ]
            - landmarks, for wich the embedding is returned
        returns: Coroutine List[NamedTuple["embedding": List[float]]]
        """
        # TODO validate json_params
    
        async with cls._db_engine.begin() as connection:
            embeddings_list = EmbeddingsReader.read_landmarks_embeddings(connection, json_params["landmarks"])
        return embeddings_list


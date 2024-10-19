# Author: Vodohleb04
"""
Embeddings CRUD module.
SELECT, INSERT, UPDATE and DELETE queries to embeddings database

https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
"""
import sqlalchemy
from typing import Dict, List
from jsonschema import validate, ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from backend.agents.landmark_embeddings_crud.pure_landmark_embeddings_crud_agent import PureLandmarkEmbeddingsCRUDAgent
from backend.agents.landmark_embeddings_crud.landmark_embeddings_crud_validation import get_landmarks_embeddings


class LandmarkEmbeddingsCRUD(PureLandmarkEmbeddingsCRUDAgent):
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
    @staticmethod
    async def _read_landmarks_embeddings(db_connection: AsyncConnection, landmarks: List[Dict[str, float | str]]):
        """
        Read query to get embeddings of the given landmarks.

        ###
        1. db_connection: sqlalchemy.ext.asyncio.AsyncConnection
            - async connection to the embeddings database
        2. landmarks: List[
            Dict[
                "name": str,
                "latitude": float,
                "longitude": float
            ]
        ]
            - landmarks, for wich the embedding is returned
        returns: List[List[float]] - List of embeddings of the given landmarks
        """
        select_query = sqlalchemy.text(
            """
            SELECT landmarks_embeddings.embedding
                FROM ostis_govno.landmarks_embeddings AS landmarks_embeddings
                WHERE 
                    landmarks_embeddings.name = :name AND
                    landmarks_embeddings.latitude = :latitude AND
                    landmarks_embeddings.longitude = :longitude;
            """
        )
        result = [None for _ in range(len(landmarks))]
        for i in range(len(landmarks)):
            result[i] = (
                await db_connection.execute(
                    select_query,
                    landmarks[i]
                )
            ).first().embedding

        return result


    async def get_landmarks_embeddings(self, json_params: Dict):
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
        try:
            validate(json_params, get_landmarks_embeddings)
        except ValidationError as ex:
            return [] # raise ValidationError
    
        async with self._db_engine.begin() as connection:
            embeddings_list = await self._read_landmarks_embeddings(connection, json_params["landmarks"])
        return embeddings_list


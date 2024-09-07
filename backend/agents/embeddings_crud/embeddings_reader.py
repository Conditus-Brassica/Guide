# Author: Vodohleb04
from typing import List, Dict
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncConnection


class EmbeddingsReader:

    @staticmethod
    async def read_landmarks_embeddings(db_connection: AsyncConnection, landmarks: List[Dict[str, float | str]]):
        """
        Read query to get embeddings of the given landmarks.

        ###
        1. db_connection: sqlalchemy.ext.asyncio.AsyncConnection
            - async connection to the embeddings database
        2. landmarks_list: List[
            Dict[
                "name": str,
                "latitude": float,
                "longitude": float
            ]
        ]
            - landmarks, for wich the embedding is returned
        returns: List[NamedTuple["embedding": List[float]]]
        """
        select_query = sqlalchemy.text(
            """
            SELECT landmarks_embeddings.embedding
                FROM ostis_govno.landmarks_embeddings AS landmarks_embeddings
                WHERE 
                    landmarks_embeddings.name = :name AND
                    landmarks_embeddings.latitude = :latitude AND
                    landmarss_embeddings.longitude = :longitude;
            """
        )
        result = [None for _ in range(len(landmarks))]
        for i in range(len(landmarks)):
            result[i] = (
                await db_connection.execute(
                    select_query,
                    landmarks[i]
                )
            ).first()

        return result


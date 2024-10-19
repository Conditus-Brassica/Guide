# Author: Vodohleb04
"""
Embeddings CRUD module.
SELECT, INSERT, UPDATE and DELETE queries to embeddings database

https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
"""
from typing import Dict
from jsonschema import validate, ValidationError
from chromadb.api.models import AsyncCollection
from backend.agents.note_embeddings_crud.pure_note_embeddings_crud_agent import PureNoteEmbeddingsCRUDAgent
from backend.agents.note_embeddings_crud.note_embeddings_crud_validation import get_nearest_notes


class NoteEmbeddingsCRUD(PureNoteEmbeddingsCRUDAgent):
    """
    Class to work with embeddings database. Provides read, write, update and delete queries for embeddings database.
    All methods work asynchronously.
    
    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s
    """
    
    _single_embeddings_crud = None
    _search_collection: AsyncCollection = None
    _embedding_collection: AsyncCollection = None
    _embeddings_include = ["ids", "embeddings"]
    _without_embeddings_include = ["ids"]

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
    def _class_init(cls, search_collection: AsyncCollection, embedding_collection: AsyncCollection):
        cls._search_collection = search_collection
        cls._embedding_collection = embedding_collection

    def __init__(self, search_collection: AsyncCollection, embedding_collection: AsyncCollection):
        """
        Class to work with embeddings database. Provides read, write, update and delete queries for embeddings database
    
        https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s

        ###
        1. search_collection: chromadb.api.models.AsyncCollection
            - AsyncCollection, that provides connection to collection with embeddings used in informational search
        2. embedding_collection: chromadb.api.models.AsyncCollection
            - AsyncCollection, that provides connection to collection with embeddings used in recommendation system
        """
        if not self._single_embeddings_crud:
            self._class_init(search_collection, embedding_collection)
            self._single_embeddings_crud = self
        else:
            RuntimeError("Unexpected behaviour, this class can have only one instance")

    # Read queries


    async def get_nearest_notes(self, json_params: Dict):
        try:
            validate(json_params, get_nearest_notes)
            if json_params["limit"] >= 0:
                raise ValidationError(f"Expected limit to be int in range [1, ..], but got {json_params['limit']} instead")
        except ValidationError as ex:
            return {"note_titles": []} # raise ValidationError
        return_embeddings = json_params.get("return_embeddings", False)

        result = await self._embedding_collection.query(
            query_embeddings=[json_params["note_embeddings"]],
            n_results=json_params["limit"],
            include=self._embeddings_include if return_embeddings else self._without_embeddings_include
        )
        if return_embeddings:
            return {
                "note_titles": result["ids"][0],  # List if ids
                "embeddings": result["embeddings"][0]  # List nearest embeddings
            }
        else:
            return {"note_titles": result["ids"][0]}



# Author: Vodohleb04
"""
Embeddings CRUD module.
SELECT, INSERT, UPDATE and DELETE queries to embeddings database

https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1311s
"""
import asyncio
from typing import Dict
from aiologger.loggers.json import JsonLogger
from jsonschema import validate, ValidationError
from chromadb.api.models.AsyncCollection import AsyncCollection
from backend.agents.note_embeddings_crud.pure_note_embeddings_crud_agent import PureNoteEmbeddingsCRUDAgent
from backend.agents.note_embeddings_crud.note_embeddings_crud_validation import (
    get_nearest_notes, add_note_embedding, update_note_embedding, delete_notes
)


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class NoteEmbeddingsCRUD(PureNoteEmbeddingsCRUDAgent):
    """
    Class to work with embeddings database. Provides read, write, update and delete queries for embeddings database.
    All methods work asynchronously.
    
    https://www.youtube.com/watch?v=kDnJf-bFTaY&t=1328s
    """
    
    _single_embeddings_crud = None
    _embeddings_include = ["embeddings"]
    _without_embeddings_include = []

    @classmethod
    def get_embeddings_crud(cls):
        return cls._single_embeddings_crud
    
    @classmethod
    def embeddings_crud_exists(cls) -> bool:
        if cls._single_embeddings_crud:
            return True
        else:
            return False


    def __init__(self, embedding_collection: AsyncCollection):
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
            self._embedding_collection: AsyncCollection = embedding_collection

            self._single_embeddings_crud = self
        else:
            RuntimeError("Unexpected behaviour, this class can have only one instance")

    # Read queries

    async def get_nearest_notes(self, json_params: Dict):
        try:
            validate(json_params, get_nearest_notes)
            if json_params["limit"] < 0:
                raise ValidationError(f"Expected limit to be int in range [1, ..], but got {json_params['limit']} instead")
        except ValidationError as ex:
            return {"note_titles": []} # raise ValidationError
        return_embeddings = json_params.get("return_embeddings", False)

        result = await self._embedding_collection.query(
            query_embeddings=[json_params["note_embedding"]],
            n_results=json_params["limit"],
            include=self._embeddings_include if return_embeddings else self._without_embeddings_include
        )
        if return_embeddings:
            return {
                "note_titles": result["ids"][0],  # List of ids
                "embeddings": result["embeddings"][0]  # List of nearest embeddings
            }
        else:
            return {"note_titles": result["ids"][0]}


    # Write queries
    async def add_note_embedding(self, json_params: Dict):
        try:
            validate(json_params, add_note_embedding)
        except ValidationError as ex:
            return {"result": False}  # raise ValidationError

        try:
            await self._embedding_collection.add(
                ids=[json_params["note_title"]],
                embeddings = [json_params["note_embedding"]]
            )
            return {"result": True}
        except Exception as ex:
            logger.error(f"Exception occurred: {ex.args}")
            return {"result": False}


    # Update queries
    async def update_note_embedding(self, json_params: Dict):
        try:
            validate(json_params, update_note_embedding)
        except ValidationError as ex:
            return {"result": False}  # raise ValidationError

        try:
            await self._embedding_collection.update(
                ids=[json_params["note_title"]],
                embeddings=[json_params["note_embedding"]]
            )
            return {"result": True}
        except Exception as ex:
            logger.error(f"Exception occurred: {ex.args}")
            return {"result": False}


    # Delete queries
    async def delete_notes_embeddings(self, json_params: Dict):
        try:
            validate(json_params, delete_notes)
        except ValidationError as ex:
            return {"result": False}  # raise ValidationError

        try:
            await self._embedding_collection.delete(
                ids=json_params["note_title_list"]
            )
            return {"result": True}
        except Exception as ex:
            logger.error(f"Exception occurred: {ex.args}")
            return {"result": False}


if __name__ == "__main__":
    import asyncio
    import chromadb

    async def main():
        embedding_db_client = await chromadb.AsyncHttpClient(
            host="localhost", port=8000
        )
        embedding_collection = await embedding_db_client.get_or_create_collection(
            name="note_embedding_collection", metadata={"hnsw:space": "cosine"}
        )
        note_emb_ag = NoteEmbeddingsCRUD(embedding_collection)

        emb1 = [1., 1., 1.]
        emb2 = [3., 3.9, 3.1]
        emb3 = [0, -1, 0.5]
        await note_emb_ag.add_note_embedding({"note_title": "1", "note_embedding": emb1})
        await note_emb_ag.add_note_embedding({"note_title": "2", "note_embedding": emb2})
        await note_emb_ag.add_note_embedding({"note_title": "3", "note_embedding": emb3})

        res = await note_emb_ag.get_nearest_notes({"note_embedding": [1., 1., 1.], "return_embeddings": True, "limit": 3})
        print(res)

        print(await embedding_collection.get(include=["embeddings"]))

        await note_emb_ag.update_note_embedding({"note_title": "1", "note_embedding": [-1., -1., -1.]})
        print(await embedding_collection.get(include=["embeddings"]))

        res = await note_emb_ag.get_nearest_notes({"note_embedding": [1., 1., 1.], "return_embeddings": True, "limit": 3})
        print(res)

        await note_emb_ag.delete_notes_embeddings({"note_title_list": ["3", "2"]})
        print(await embedding_collection.get(include=["embeddings"]))
        await note_emb_ag.delete_notes_embeddings({"note_title_list": ["3", "2"]})
        print(await embedding_collection.get(include=["embeddings"]))
        await embedding_collection.delete((await embedding_collection.get())["ids"])

    asyncio.run(main())
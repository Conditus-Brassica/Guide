# Author: Vodohleb04
"""
Tasks to work with embeddings crud agent
"""

from typing import Dict
from backend.broker.broker_initializer import BROKER
from backend.agents.note_embeddings_crud.note_embeddings_crud_initializer import NOTE_EMBEDDINGS_CRUD_AGENT


# Write tasks
@BROKER.task
async def add_note_embedding(json_params: Dict):
    """
        Write query to add embedding of the note to the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title": str,
            "note_embedding": List[float]
        ]

        :return: Coroutine Dict{"result": bool}, True, if is successfully added
    """
    return await NOTE_EMBEDDINGS_CRUD_AGENT.add_note_embedding(json_params)


# Read tasks
@BROKER.task
async def get_nearest_notes(json_params: Dict):
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
    return await NOTE_EMBEDDINGS_CRUD_AGENT.get_nearest_notes(json_params)


# Update tasks
@BROKER.task
async def update_note_embedding(json_params: Dict):
    """
        Update query to update embedding of the note, stored in the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title": str,
            "note_embedding": List[float]
        ], where note_embedding is the new embedding of the given note.

        :return: Coroutine Dict["result": bool], True if is successfully updated.
    """
    return await NOTE_EMBEDDINGS_CRUD_AGENT.update_note_embedding(json_params)


# Update tasks
@BROKER.task
async def delete_notes_embeddings(json_params: Dict):
    """
        Delete query to remove the given notes from the database.
        Works asynchronously

        :param json_params: Dict[
            "note_title_list": List[str]
        ]

        :return: Coroutine Dict["result": True]
    """
    return await NOTE_EMBEDDINGS_CRUD_AGENT.delete_notes_embeddings(json_params)

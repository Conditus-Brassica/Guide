# Author: Vodohleb04

import chromadb
from backend.agents.note_embeddings_crud.note_embeddings_crud_agent import NoteEmbeddingsCRUD

if LandmarkEmbeddingsCRUD.embeddings_crud_exists():
    NOTE_EMBEDDINGS_CRUD_AGENT = NoteEmbeddingsCRUD.get_embeddings_crud()
    print("Embeddings crud is already exists")
else:
    embedding_db_client = await chromadb.AsyncHttpClient(
        host="localhost", port=1000
    )
    embedding_collection = await embedding_db_client.get_or_create_collection(
        name="note_embedding_collection", metadata={"hnsw:space": "cosine"}
    )
    NOTE_EMBEDDINGS_CRUD_AGENT = NoteEmbeddingsCRUD(embedding_collection)
    print("Embeddings crud was created")
    

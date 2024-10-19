# Author: Vodohleb04

from sqlalchemy.ext.asyncio import create_async_engine
from backend.agents.landmark_embeddings_crud.landmark_embeddings_crud_agent import LandmarkEmbeddingsCRUD


if LandmarkEmbeddingsCRUD.embeddings_crud_exists():
    LANDMARK_EMBEDDINGS_CRUD_AGENT = LandmarkEmbeddingsCRUD.get_embeddings_crud()
    print("Embeddings crud is already exists")
else:
    db_engine = create_async_engine("postgresql+asyncpg://postgres:ostisGovno@0.0.0.0:5432/postgres")
    LANDMARK_EMBEDDINGS_CRUD_AGENT = LandmarkEmbeddingsCRUD(db_engine)
    print("Embeddings crud was created")
    

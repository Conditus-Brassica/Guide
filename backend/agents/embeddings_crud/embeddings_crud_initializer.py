# Author: Vodohleb04

from sqlalchemy.ext.asyncio import create_async_engine
from backend.agents.embeddings_crud.embeddings_crud_agent import EmbeddingsCRUD


if EmbeddingsCRUD.embeddings_crud_exists():
    EMBEDDINGS_CRUD_AGENT = EmbeddingsCRUD.get_embeddings_crud()
    print("Embeddings crud is already exists")
else:
    db_engine = create_async_engine("postgresql+asyncpg://postgres:ostisGovno@0.0.0.0:5432/postgres")
    EMBEDDINGS_CRUD_AGENT = EmbeddingsCRUD(db_engine)
    print("Embeddings crud was created")
    

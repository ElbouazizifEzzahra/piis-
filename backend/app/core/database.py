from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# 1. Create the engine 
engine = create_engine(settings.DATABASE_URL)

# 2. Dependency for API Routes 
def get_session():
    with Session(engine) as session:
        yield session

# 3. Create Tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_recreate():
    SQLModel.metadata.drop_all(engine)    
    SQLModel.metadata.create_all(engine)

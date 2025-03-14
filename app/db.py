from typing import Annotated
from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
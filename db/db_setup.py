from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    """
    Dependency that provides a SQLModel session for database operations.
    Yields a session object to be used in API endpoints.
    """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
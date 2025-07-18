from typing import List, Annotated
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.db_setup import SessionDep
from db.models.user import User, UserCreate, UserPublic, UserUpdate
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=['users'])

@router.get("/users", response_model=List[UserPublic])
async def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@router.post("/users", response_model=UserPublic)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=422, detail="Email already exists")
    session.refresh(db_user)
    return db_user

@router.get("/users/{id}", response_model=UserPublic)
async def get_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{id}", response_model=UserPublic)
async def update_user(id: int, user: UserUpdate, session: SessionDep):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/users/{id}")
async def delete_user(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
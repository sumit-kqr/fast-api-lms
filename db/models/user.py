from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr
from .mixins import Timestamp

class Role(str, Enum):
    teacher = "teacher"
    student = "student"

class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=100)
    role: Role = Field(sa_type=SAEnum(Role, name="role"))

class User(UserBase, Timestamp, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    email: Optional[str] = None
    role: Optional[Role] = None

class ProfileBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    bio: Optional[str] = None
    is_active: bool = Field(default=False)

class Profile(ProfileBase, Timestamp, table=True):
    __tablename__ = "profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")

class ProfilePublic(ProfileBase):
    id: int
    user_id: int

class ProfileCreate(ProfileBase):
    user_id: int

class ProfileUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
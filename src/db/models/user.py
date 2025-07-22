from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SAEnum
from pydantic import EmailStr
from .mixins import Timestamp

class Role(str, Enum):
    """Enum for user roles."""
    teacher = "teacher"
    student = "student"

class UserBase(SQLModel):
    """Base model for user data."""
    email: EmailStr = Field(index=True, unique=True, max_length=100)
    role: Role = Field(sa_type=SAEnum(Role, name="role"))

class User(UserBase, Timestamp, table=True):
    """SQLModel table for users."""
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)

class UserPublic(UserBase):
    """Public schema for user data."""
    id: int

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class UserUpdate(SQLModel):
    """Schema for updating user fields."""
    email: Optional[str] = None
    role: Optional[Role] = None

class ProfileBase(SQLModel):
    """Base model for user profile data."""
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    bio: Optional[str] = None
    is_active: bool = Field(default=False)

class Profile(ProfileBase, Timestamp, table=True):
    """SQLModel table for user profiles."""
    __tablename__ = "profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="users.id")

class ProfilePublic(ProfileBase):
    """Public schema for profile data."""
    id: int
    user_id: int

class ProfileCreate(ProfileBase):
    """Schema for creating a new profile."""
    user_id: int

class ProfileUpdate(SQLModel):
    """Schema for updating profile fields."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
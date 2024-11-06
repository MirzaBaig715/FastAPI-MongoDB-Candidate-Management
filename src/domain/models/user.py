from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)


class UserInDB(UserBase):
    """User database model."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class User(UserBase):
    """User response model."""
    id: str
    created_at: datetime
    updated_at: datetime

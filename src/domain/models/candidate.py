from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class CandidateBase(BaseModel):
    """Base candidate model."""
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    position: str
    experience: int = Field(..., ge=0)
    skills: list[str] = Field(default_factory=list)
    status: str = Field(..., pattern="^(applied|screening|interviewed|offered|hired|rejected)$")


class CandidateCreate(CandidateBase):
    """Candidate creation model."""
    pass


class CandidateUpdate(CandidateBase):
    """Candidate update model."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    position: Optional[str] = None
    experience: Optional[int] = None
    skills: Optional[list[str]] = None
    status: Optional[str] = None


class CandidateInDB(CandidateBase):
    """Candidate database model."""
    id: str = Field(default_factory=lambda: str(ObjectId()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Candidate(CandidateBase):
    """Candidate response model."""
    id: str
    created_at: datetime
    updated_at: datetime

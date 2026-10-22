from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.domain import RoleEnum, RequestStatusEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: RoleEnum = RoleEnum.CITIZEN
    phone: Optional[str] = None
    preferred_language: str = "en"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: RoleEnum
    preferred_language: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CommunityRequestCreate(BaseModel):
    title: str
    description: str
    category: str
    urgency: str = "MEDIUM"
    location_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CommunityRequestResponse(BaseModel):
    id: UUID
    requester_id: UUID
    title: str
    description: str
    category: str
    urgency: str
    status: RequestStatusEnum
    location_name: str
    quality_score: float
    is_duplicate: bool
    created_at: datetime

    class Config:
        from_attributes = True
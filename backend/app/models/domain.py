import uuid
import enum
from sqlalchemy import Column, String, Float, Boolean, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.db.session import Base

class RoleEnum(str, enum.Enum):
    CITIZEN = "CITIZEN"
    VOLUNTEER = "VOLUNTEER"
    ORGANIZER = "ORGANIZER"
    DONOR = "DONOR"
    ADMIN = "ADMIN"

class RequestStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    VERIFIED = "VERIFIED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.CITIZEN)
    phone = Column(String(50), nullable=True)
    preferred_language = Column(String(10), nullable=False, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requests = relationship("CommunityRequest", back_populates="requester")

class CommunityRequest(Base):
    __tablename__ = "community_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    urgency = Column(String(50), nullable=False, default="MEDIUM")
    status = Column(SQLEnum(RequestStatusEnum), nullable=False, default=RequestStatusEnum.PENDING)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # AI Pipeline Metadata
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(UUID(as_uuid=True), ForeignKey("community_requests.id"), nullable=True)
    quality_score = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    requester = relationship("User", back_populates="requests")
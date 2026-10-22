from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.domain import User, CommunityRequest
from app.schemas.schemas import CommunityRequestCreate, CommunityRequestResponse
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CommunityRequestResponse)
def create_request(
    req_in: CommunityRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    req = CommunityRequest(
        requester_id=current_user.id,
        title=req_in.title,
        description=req_in.description,
        category=req_in.category,
        urgency=req_in.urgency,
        location_name=req_in.location_name,
        latitude=req_in.latitude,
        longitude=req_in.longitude
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@router.get("/", response_model=List[CommunityRequestResponse])
def list_requests(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(CommunityRequest).offset(skip).limit(limit).all()
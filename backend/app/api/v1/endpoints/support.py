from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.ai.vision_verifier import VisionEvidenceVerifier
from app.services.matching_engine import SmartMatchingEngine

router = APIRouter()

class VolunteerInput(BaseModel):
    id: str
    full_name: str
    skills: List[str]
    latitude: float
    longitude: float

class MatchRequest(BaseModel):
    category: str
    urgency: str = "MEDIUM"
    latitude: float
    longitude: float
    volunteers: List[VolunteerInput]

@router.post("/verify-evidence")
async def verify_evidence(file: UploadFile = File(...)):
    contents = await file.read()
    result = VisionEvidenceVerifier.verify_image_quality(contents)
    return result

@router.post("/match-volunteers")
def match_volunteers(payload: MatchRequest):
    req_dict = {
        "category": payload.category,
        "urgency": payload.urgency,
        "latitude": payload.latitude,
        "longitude": payload.longitude
    }
    vols_dicts = [v.model_dump() for v in payload.volunteers]
    ranked = SmartMatchingEngine.rank_volunteers(req_dict, vols_dicts)
    return {"matched_volunteers": ranked}
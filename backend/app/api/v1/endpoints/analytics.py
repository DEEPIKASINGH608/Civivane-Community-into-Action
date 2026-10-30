from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.geo_service import GeospatialService
from app.websockets.manager import manager

router = APIRouter()

@router.get("/nearby")
def get_nearby_requests(lat: float, lon: float, radius: float = 10.0, db: Session = Depends(get_db)):
    nearby = GeospatialService.get_requests_within_radius(db, lat, lon, radius)
    return {"center": {"latitude": lat, "longitude": lon}, "radius_km": radius, "results": nearby}

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"event": "CLIENT_MESSAGE", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
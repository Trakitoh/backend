from fastapi import APIRouter, HTTPException, status

from app.core.database import Session
from app.ping.service import PingService
from app.ping.model import PingModel, PingRequestBody

router = APIRouter()

@router.get("/ping/{id}")
async def get_ping(id: int, session: Session) -> PingModel:
    result = await PingService.read_by_id(session, id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Ping with id={id} not found"
        )
        
    return PingService.to_model(result)

@router.post("/ping")
async def create_ping(body: PingRequestBody, session: Session) -> PingModel:
    # **: unpacks dictionary key values
    # model_dump(): converts Pydantic model into dictionary
    # exclude_none(): ignores all None values
    #raw_data = PingRequestBody(**body.model_dump(exclude_none=True))
    raw_ping = PingService.to_orm(body)
    
    result = await PingService.create(session, raw_ping)
    
    return PingService.to_model(result)
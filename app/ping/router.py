from fastapi import APIRouter, HTTPException, status

from app.core.database import Session
from app.ping.service import PingService
from app.ping.model import PingModel, PingRaw

router = APIRouter()

@router.get("/ping")
async def get_pings(session:Session):
    results = await PingService.read(session)
    
    return results

@router.get("/ping/random")
async def get_ping_random(session: Session) -> PingModel:
    result = await PingService.read_random(session)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No pings found!"
        )
        
    return result


@router.get("/ping/{id}")
async def get_ping(id: int, session: Session) -> PingModel:
    result = await PingService.read_by_id(session, id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Ping with id={id} not found"
        )
        
    return result

@router.post("/ping")
async def create_ping(body: PingRaw, session: Session) -> PingModel:
    # **: unpacks dictionary key values
    # model_dump(): converts Pydantic model into dictionary
    # exclude_none(): ignores all None values
    #raw_data = PingRaw(**body.model_dump(exclude_none=True))
    
    result = await PingService.create(session, body)
    
    return result

@router.put("/ping/{id}")
async def update_ping(id: int, body: PingRaw, session: Session) -> PingModel:
    result = await PingService.update(session, id, body)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Ping with id={id} not found"
        )
    
    return result

@router.delete("/ping/{id}", status_code=200)
async def delete_ping(id: int, session: Session):
    deleted = await PingService.delete_by_id(session, id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No pings deleted. Ping with ID #{id} not found."
        )
        
    return {"detail": f"Ping with ID #{id} was deleted."}
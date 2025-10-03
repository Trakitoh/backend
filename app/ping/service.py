from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.ping.model import PingModel, PingRaw
from app.ping.orm import PingORM

class PingService():
    @staticmethod
    def to_orm(model: PingModel | PingRaw) -> PingORM:
        return PingORM(msg=model.msg)
    
    @staticmethod
    def to_model(orm: PingORM):
        return PingModel(id=orm.id, msg=orm.msg, created_at=orm.created_at, updated_at=orm.updated_at)
    
    @staticmethod
    async def read(session: AsyncSession):
        results = await session.execute(select(PingORM))
        
        # returns empty list if no results
        entities = results.scalars().all()
        
        if len(entities) == 0:
            return []
        
        return [PingService.to_model(m) for m in entities]        
    
    @staticmethod
    async def read_by_id(session: AsyncSession, id: int):
        # result = await session.execute(select(PingORM).where(PingORM.id == id))
        # return result.scalar()
        
        result = await session.get(PingORM, id)
        
        if not result:
            return None
        
        return PingService.to_model(result)
    
    @staticmethod
    async def read_random(session: AsyncSession):
        result = await session.execute(select(PingORM).order_by(func.random()).limit(1))
        
        entity = result.scalar()
        
        if not entity:
            return None
        
        return PingService.to_model(entity)
    
    # TODO: add exception handling for failed to create
    @staticmethod
    async def create(session: AsyncSession, data: PingRaw):
        new_ping = PingService.to_orm(data)
        
        session.add(new_ping)
        await session.commit()
        await session.refresh(new_ping)
                
        return PingService.to_model(new_ping)
    
    @staticmethod
    async def update(session: AsyncSession, id: int, data: PingRaw):
        updated_ping = await session.get(PingORM, id)
        
        if not updated_ping:
            return None
        
        updated_ping.msg = data.msg
        current_timestamp = await session.execute(select(func.now()))
        ts = current_timestamp.scalar()
        updated_ping.updated_at = ts
        
        await session.commit()
        await session.refresh(updated_ping)
        
        return PingService.to_model(updated_ping)
    
    @staticmethod
    async def delete_by_id(session: AsyncSession, id: int):
        
        result = await session.get(PingORM, id)
        
        if result:
            # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncSession.delete
            #   - https://docs.sqlalchemy.org/en/20/orm/session_basics.html#deleting
            await session.delete(result)
            await session.commit()
            return True
        
        return False
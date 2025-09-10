from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.ping.model import PingModel, PingRequestBody
from app.ping.orm import PingORM

class PingService():
    @staticmethod
    def to_orm(model: PingModel | PingRequestBody) -> PingORM:
        return PingORM(msg=model.msg)
    
    @staticmethod
    def to_model(orm: PingORM):
        return PingModel(id=orm.id, msg=orm.msg)
    
    @staticmethod
    async def create(session: AsyncSession, new_ping: PingORM):
        session.add(new_ping)
        await session.commit()
        await session.refresh(new_ping)
        
        return new_ping
    
    @staticmethod
    async def read_by_id(session: AsyncSession, id: int):
        result = await session.execute(select(PingORM).where(PingORM.id == id))
        return result.scalar()
    
from typing import Optional
from datetime import datetime
from sqlalchemy import func, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class PingORM(Base):
    __tablename__ = "Ping"
    id: Mapped[int] = mapped_column(primary_key=True)
    msg: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]]
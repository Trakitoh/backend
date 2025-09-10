from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class PingORM(Base):
    __tablename__ = "Ping"
    id: Mapped[int] = mapped_column(primary_key=True)
    msg: Mapped[str]
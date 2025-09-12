from datetime import datetime
from pydantic import BaseModel, Field

class PingRaw(BaseModel):
    msg: str = Field(max_length=255)
    
class PingModel(PingRaw):
    id: int
    created_at: datetime
    updated_at: datetime | None = Field(default=None)
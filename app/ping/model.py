from pydantic import BaseModel

class PingRequestBody(BaseModel):
    msg: str
    
class PingModel(BaseModel):
    id: int
    msg: str
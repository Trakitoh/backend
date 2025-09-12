from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.ping.router import router as pingrouter

# Used for setup (before app starts) & teardown (after app ends)
@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting Trakito backend...")
    await init_db() # setup db connection & table create b4 fastapi starts
    yield # start fastapi here
    print("...stopping Trakito backend")

app = FastAPI(lifespan=lifespan_handler)
app.include_router(pingrouter)

@app.get("/")
async def root():
    return {"message": "Hello World!"}
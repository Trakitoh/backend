from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs

# TODO: setup URL loading via environment variable config
# Engine is responsible for database connection managemnet
engine = create_async_engine(url="sqlite+aiosqlite:///dev.db")
# expire_on_commit prevents database calls to refresh entity
#    - needed for async since all db calls must be awaited (?); and implicit db calls aren't async
# session is ORM interface for interacting with database tables & entities
sesh = async_sessionmaker(engine, expire_on_commit=False)

# Needed to establish ORM models/tables
# AsyncAttrs is to enable async loading of attributes that are lazy loaded by default
class Base(AsyncAttrs, DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        # Base class is the parent class for ORM models
        #   - it contains MetaData object, that is registry for all db Table objects associated with ORM models
        #   - create_all() causes SQLAlchemy to iterate through all Table objects and issue "CREATE_TABLE" SQL commands
        # Creates database tables based on ORM models
        await conn.run_sync(Base.metadata.create_all)

# Gets session instance for DB operations
# Establishes session that will close after calling function returns
#   - must close session since the same session cannot be used in multiple tasks concurrently
# Note, async ORM requires overriding defaults to prevent implicit IO (aka lazy loading)
#   - see: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#asyncio-orm-avoid-lazyloads
async def get_session():
    # For "conn, session.begin()",
    #   - see https://docs.sqlalchemy.org/en/20/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
    async with sesh() as session, sesh.begin():
        yield session # returns session object for database operations

# Enables DI for session instances
#   - see: https://fastapi.tiangolo.com/tutorial/dependencies/
Session = Annotated[AsyncSession, Depends(get_session)]


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from src.database.repo.requests import RequestsRepo
from src.database.setup import create_engine, create_session_pool

engine = create_engine(config.db)
session_pool = create_session_pool(engine)

async def get_session() -> AsyncSession:
    session = session_pool()
    try:
        yield session
    finally:
        await session.close()

async def get_repo(session: AsyncSession = Depends(get_session)) -> RequestsRepo:
    yield RequestsRepo(session)
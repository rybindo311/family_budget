from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession)

from config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo = True,
)

new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

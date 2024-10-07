import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from .engine import async_session_factory


@contextlib.asynccontextmanager
async def create_session() -> AsyncIterator[AsyncSession]:
    """Dependency с сессией SQLAlchemy.

    Yields:
        Iterator[AsyncIterator[AsyncSession]]: открытая через контекстный менеджер сессия.
    """
    async with async_session_factory.begin() as session:
        yield session

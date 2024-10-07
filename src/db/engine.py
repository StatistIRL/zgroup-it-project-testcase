from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from settings import DatabaseSettings, get_settings

settings: DatabaseSettings = get_settings(DatabaseSettings)
engine: AsyncEngine = create_async_engine(url=settings.url)
async_session_factory = async_sessionmaker(bind=engine)

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config_data.config import config

engine = create_async_engine(f"sqlite+aiosqlite:///{config.database.database}", echo=True)
session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        from .models import User
        await conn.run_sync(Base.metadata.create_all)
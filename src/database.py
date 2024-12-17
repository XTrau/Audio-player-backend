from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(url=settings.db.DATABASE_URL_asyncpg)

new_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with new_session() as session:
        yield session


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as conn:
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        await conn.execute(query)
        await conn.run_sync(Base.metadata.create_all)

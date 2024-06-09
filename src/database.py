from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

print(settings.DATABASE_URL_asyncpg)

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg
)

new_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import UserOrm
from auth.schemas import SUserCreate
from database import get_async_session


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: SUserCreate, hashed_password: str) -> UserOrm:
        user_model = UserOrm(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        self.session.add(user_model)
        await self.session.flush()
        await self.session.commit()
        return user_model

    async def find_by_id(self, user_id: int) -> UserOrm:
        query = select(UserOrm).where(UserOrm.id == user_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def find_by_email(self, email: str) -> UserOrm:
        query = select(UserOrm).where(UserOrm.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def find_by_username(self, username: str) -> UserOrm:
        query = select(UserOrm).where(UserOrm.username == username)
        result = await self.session.execute(query)
        return result.scalar()


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session)

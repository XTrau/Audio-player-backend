from sqlalchemy import select
from src.auth.models import UserOrm
from src.auth.schemas import SUserCreate
from src.database import new_session


class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalar()
            return user

    @staticmethod
    async def create_user(user: SUserCreate):
        async with new_session() as session:
            user_model = UserOrm(
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
            )
            session.add(user_model)
            await session.flush()
            await session.commit()
            return user_model

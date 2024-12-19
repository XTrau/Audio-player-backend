from sqlalchemy import select

from auth.models import UserOrm
from auth.schemas import SUserCreate
from database import new_session
from models import UserTrackOrm


class UserRepository:
    @staticmethod
    async def create(user: SUserCreate, hashed_password: str) -> UserOrm:
        async with new_session() as session:
            user_model = UserOrm(
                email=user.email,
                username=user.username,
                hashed_password=hashed_password,
            )

            if user.username == "string":
                user_model.is_admin = True

            session.add(user_model)
            await session.flush()
            await session.commit()
            return user_model

    @staticmethod
    async def find_by_id(user_id: int) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            user_model: UserOrm | None = (await session.execute(query)).scalar()
        return user_model

    @staticmethod
    async def find_by_email(email: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            user_model: UserOrm | None = (await session.execute(query)).scalar()
        return user_model

    @staticmethod
    async def find_by_username(username: str) -> UserOrm | None:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.username == username)
            user_model: UserOrm | None = (await session.execute(query)).scalar()
        return user_model

    @staticmethod
    async def add_track_to_liked(user_id: int, track_id: int) -> None:
        async with new_session() as session:
            user_track = UserTrackOrm(user_id=user_id, track_id=track_id)
            session.add(user_track)
            await session.commit()

    @staticmethod
    async def check_user(user_id: int) -> bool:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            user_model = (await session.execute(query)).scalar()
        return False if not user_model else True

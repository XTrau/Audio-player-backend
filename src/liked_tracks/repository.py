from sqlalchemy import select, delete, and_
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, status

from auth.models import UserOrm
from database import new_session
from models import UserTrackOrm
from tracks.models import TrackOrm


class UserLikesRepository:
    @staticmethod
    async def get_liked_tracks(user_id: int) -> list[TrackOrm]:
        async with new_session() as session:
            query = (
                select(UserOrm)
                .where(UserOrm.id == user_id)
                .options(
                    selectinload(UserOrm.liked_tracks).options(
                        joinedload(TrackOrm.album),
                        selectinload(TrackOrm.artists),
                    )
                )
            )
            result = await session.execute(query)
            return result.scalar().liked_tracks

    @staticmethod
    async def get_liked_track_ids(user_id: int) -> list[int]:
        async with new_session() as session:
            query = select(UserTrackOrm.track_id).where(UserTrackOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def like_track(user_id: int, track_id: int) -> None:
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            result = await session.execute(query)
            model = result.scalar()
            if model is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Указанный трек не найден",
                )

            query = select(UserTrackOrm).where(
                and_(UserTrackOrm.user_id == user_id, UserTrackOrm.track_id == track_id)
            )
            result = await session.execute(query)
            model = result.scalar()
            if model is None:
                model = UserTrackOrm(track_id=track_id, user_id=user_id)
                session.add(model)
                await session.commit()

    @staticmethod
    async def unlike_track(user_id: int, track_id: int):
        async with new_session() as session:
            stmt = delete(UserTrackOrm).where(
                and_(UserTrackOrm.user_id == user_id, UserTrackOrm.track_id == track_id)
            )
            await session.execute(stmt)
            await session.commit()

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload

from database import new_session
from file_manager import save_file

from models import TrackPlaylistOrm
from auth.models import UserOrm
from playlist.models import PlaylistOrm
from tracks.models import TrackOrm

from playlist.schemas import SPlaylistCreate


playlist_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Указанный плейлист не найден"
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Указанный пользователь не найден"
)

track_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Указанный трек не найден"
)


class PlaylistRepository:
    @staticmethod
    async def create_playlist(playlist: SPlaylistCreate, user_id: int) -> PlaylistOrm:
        async with new_session() as session:
            track_ids = set(playlist.track_ids)
            query = select(TrackOrm).where(TrackOrm.id.in_(track_ids))
            existing_tracks = await session.execute(query)
            existing_track_ids = {row[0] for row in existing_tracks}

            image_file_name = await save_file(
                playlist.image_file, ["jpg", "jpeg", "png"], playlist.title
            )

            playlist_model = PlaylistOrm(
                title=playlist.title,
                image_file_name=image_file_name,
                creator_id=user_id,
            )
            session.add(playlist_model)
            await session.flush()

            track_playlist_models = [
                TrackPlaylistOrm(track_id=track_id, playlist_id=playlist_model.id)
                for track_id in existing_track_ids
            ]
            session.add_all(track_playlist_models)
            await session.commit()
            return playlist_model

    @staticmethod
    async def get_playlist(playlist_id: int) -> PlaylistOrm:
        async with new_session() as session:
            query = (
                select(PlaylistOrm)
                .where(PlaylistOrm.id == playlist_id)
                .options(
                    selectinload(PlaylistOrm.tracks).options(
                        selectinload(TrackOrm.artists)
                    )
                )
            )
            result = await session.execute(query)
            playlist_model = result.scalar()
            return playlist_model

    @staticmethod
    async def get_created_by_user_playlists(user_id: int) -> list[PlaylistOrm]:
        async with new_session() as session:
            query = select(PlaylistOrm).where(PlaylistOrm.creator_id == user_id)
            result = await session.execute(query)
            playlist_models = result.scalars()
            return playlist_models

    @staticmethod
    async def update_playlist(playlist_id: int, new_playlist: SPlaylistCreate) -> None:
        async with new_session() as session:
            stmt = (
                update(PlaylistOrm)
                .where(PlaylistOrm.id == playlist_id)
                .values(title=new_playlist.title)
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def delete_playlist(playlist_id: int) -> None:
        async with new_session() as session:
            stmt = delete(PlaylistOrm).where(PlaylistOrm.id == playlist_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_track_to_playlist(playlist_id: int, track_id: int) -> None:
        async with new_session() as session:
            track_playlist_model = TrackPlaylistOrm(
                track_id=track_id, playlist_id=playlist_id
            )
            session.add(track_playlist_model)
            await session.commit()

    @staticmethod
    async def delete_track_from_playlist(playlist_id: int, track_id: int) -> None:
        async with new_session() as session:
            stmt = delete(TrackPlaylistOrm).where(
                and_(
                    TrackPlaylistOrm.track_id == track_id,
                    TrackPlaylistOrm.playlist_id == playlist_id,
                )
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def check_playlist(playlist_id: int) -> bool:
        async with new_session() as session:
            query = select(PlaylistOrm).where(PlaylistOrm.id == playlist_id)
            playlist_model = (await session.execute(query)).scalar()
        return False if not playlist_model else True

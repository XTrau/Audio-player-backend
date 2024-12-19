from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from database import new_session
from playlist.repository import track_not_found_exception
from tracks.schemas import STrackCreate
from file_manager import save_file, delete_file

from models import ArtistTrackOrm
from tracks.models import TrackOrm


class TracksRepository:
    @staticmethod
    async def get_tracks(page: int, size: int) -> list[TrackOrm]:
        async with new_session() as session:
            query = (
                select(TrackOrm)
                .options(joinedload(TrackOrm.album), selectinload(TrackOrm.artists))
                .limit(size)
                .offset(page * size)
            )
            res = await session.execute(query)
            track_models: list[TrackOrm] = res.unique().scalars().all()
            return track_models

    @staticmethod
    async def get_track(track_id: int) -> TrackOrm | None:
        async with new_session() as session:
            query = (
                select(TrackOrm)
                .where(TrackOrm.id == track_id)
                .options(joinedload(TrackOrm.album), selectinload(TrackOrm.artists))
            )
            res = await session.execute(query)
            track_model: TrackOrm = res.unique().scalars().first()
            return track_model

    @staticmethod
    async def create_track(track: STrackCreate):
        async with new_session() as session:
            try:
                audio_file_name: str = await save_file(
                    track.audio_file, ["mp3", "wav"], track.title
                )
                image_file_name: str | None = await save_file(
                    track.image_file, ["jpg", "jpeg", "png"], track.title
                )

                stmt = (
                    insert(TrackOrm)
                    .values(
                        title=track.title,
                        audio_file_name=audio_file_name,
                        image_file_name=image_file_name,
                        album_id=track.album_id,
                        number_at_album=track.number_at_album,
                    )
                    .returning(TrackOrm)
                )
                result = await session.execute(stmt)
                track_model: TrackOrm = result.scalar()
                await session.commit()
                return track_model
            except Exception as e:
                await delete_file(audio_file_name)
                await delete_file(image_file_name)
                await session.rollback()

    @staticmethod
    async def set_artists(track_id: int, artist_ids: list[int]):
        async with new_session() as session:
            artist_track_models = [
                ArtistTrackOrm(artist_id=artist_id, track_id=track_id)
                for artist_id in artist_ids
            ]
            session.add_all(artist_track_models)
            await session.flush()
            await session.commit()

    @staticmethod
    async def update_track(track_id: int, track: STrackCreate):
        async with new_session() as session:
            try:
                query = select(TrackOrm).where(TrackOrm.id == track_id)
                res = await session.execute(query)
                old_track = res.scalar()

                if old_track is None:
                    raise track_not_found_exception

                audio_file_name = await save_file(
                    track.audio_file, ["mp3", "wav"], track.title
                )
                image_file_name = await save_file(
                    track.image_file, ["jpg", "jpeg", "png"], track.title
                )

                stmt = (
                    update(TrackOrm)
                    .where(TrackOrm.id == track_id)
                    .values(
                        title=track.title,
                        audio_file_name=audio_file_name,
                        image_file_name=image_file_name,
                        album_id=track.album_id,
                        number_at_album=track.number_at_album,
                    )
                )
                await session.execute(stmt)

                stmt = delete(ArtistTrackOrm).where(ArtistTrackOrm.track_id == track_id)
                await session.execute(stmt)

                artist_track_models = [
                    ArtistTrackOrm(artist_id=artist_id, track_id=track_id)
                    for artist_id in track.artist_ids
                ]

                session.add_all(artist_track_models)
                await session.commit()

                await delete_file(old_track.audio_file_name)
                await delete_file(old_track.image_file_name)
            except Exception as e:
                await session.rollback()
                await delete_file(audio_file_name)
                await delete_file(image_file_name)

    @staticmethod
    async def delete_track(track_id: int) -> TrackOrm:
        async with new_session() as session:
            stmt = delete(TrackOrm).where(TrackOrm.id == track_id).returning(TrackOrm)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @staticmethod
    async def check_track(track_id: int) -> bool:
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)
            track_model = (await session.execute(query)).scalar()
        return False if not track_model else True

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from database import new_session
from schemas import STrackAdd
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
            track_models = res.unique().scalars().all()
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
            track_model = res.unique().scalars().first()
            return track_model

    @staticmethod
    async def create_track(track: STrackAdd):
        async with new_session() as session:
            audio_file_name = await save_file(
                track.audio_file, ["mp3", "wav"], track.title
            )
            image_file_name = await save_file(
                track.image_file, ["jpg", "jpeg", "png"], track.title
            )

            track_model = TrackOrm(
                title=track.title,
                audio_file_name=audio_file_name,
                image_file_name=image_file_name,
                album_id=track.album_id,
            )
            session.add(track_model)
            await session.flush()
            artist_track_models = [
                ArtistTrackOrm(artist_id=artist_id, track_id=track_model.id)
                for artist_id in track.artist_ids
            ]
            session.add_all(artist_track_models)
            await session.flush()
            await session.commit()
            return track_model.id

    @staticmethod
    async def update_track(track_id: int, track: STrackAdd):
        async with new_session() as session:
            query = select(TrackOrm).where(TrackOrm.id == track_id)

            res = await session.execute(query)
            old_track = res.scalar()

            if old_track is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Track not found"
                )

            await delete_file(old_track.audio_file_name)
            await delete_file(old_track.image_file_name)

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

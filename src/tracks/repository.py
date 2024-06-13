from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.database import new_session
from src.models import TrackOrm, ArtistTrackOrm
from src.schemas import STrackAdd
from src.file_manager import save_file


class TracksRepository:
    @staticmethod
    async def get_tracks() -> list[TrackOrm]:
        async with new_session() as session:
            query = (
                select(TrackOrm)
                .options(
                    joinedload(TrackOrm.album),
                    selectinload(TrackOrm.artists)
                )
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
                .options(
                    joinedload(TrackOrm.album),
                    selectinload(TrackOrm.artists)
                )
            )
            res = await session.execute(query)
            track_model = res.unique().scalars().first()
            return track_model

    @staticmethod
    async def create_track(track: STrackAdd):
        async with new_session() as session:
            audio_file_name = await save_file(track.audio_file, ["mp3", "wav"], track.title)
            image_file_name = await save_file(track.image_file, ["jpg", "jpeg", "png"], track.title)

            track_model = TrackOrm(
                title=track.title,
                audio_file_name=audio_file_name,
                image_file_name=image_file_name,
                album_id=track.album_id
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

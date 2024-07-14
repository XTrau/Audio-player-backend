from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from starlette import status

from src.database import new_session
from src.schemas import SArtistAdd
from src.file_manager import save_file, delete_file

from src.artists.models import ArtistOrm
from src.tracks.models import TrackOrm


class ArtistsRepository:

    @staticmethod
    async def create_artist(artist: SArtistAdd) -> int:
        async with new_session() as session:
            img_file_name = await save_file(artist.image_file, ['jpg', 'jpeg', 'png'], artist.name)
            artist_model = ArtistOrm(name=artist.name, image_file_name=img_file_name)
            session.add(artist_model)
            await session.flush()
            await session.commit()
            return artist_model.id

    @staticmethod
    async def get_artists(page: int, size: int) -> list[ArtistOrm]:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .options(
                    selectinload(ArtistOrm.albums),
                    selectinload(ArtistOrm.tracks).options(
                        selectinload(TrackOrm.artists),
                        joinedload(TrackOrm.album)
                    )
                )
                .limit(size)
                .offset(page * size)
            )
            res = await session.execute(query)
            artists = res.unique().scalars().all()
            return artists

    @staticmethod
    async def get_artist(artist_id: int) -> ArtistOrm | None:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .options(
                    selectinload(ArtistOrm.albums),
                    selectinload(ArtistOrm.tracks).options(
                        selectinload(TrackOrm.artists),
                        joinedload(TrackOrm.album)
                    )
                )
                .where(ArtistOrm.id == artist_id)
            )
            res = await session.execute(query)
            artist_model = res.unique().scalar()
            return artist_model

    @staticmethod
    async def update_artist(artist_id: int, artist: SArtistAdd) -> ArtistOrm | None:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .where(ArtistOrm.id == artist_id)
            )

            res = await session.execute(query)
            old_artist = res.scalar()
            if old_artist is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

            await delete_file(old_artist.image_file_name)

            image_file_name = await save_file(artist.image_file, ['jpg', 'jpeg', 'png'], artist.name)

            stmt = (
                update(ArtistOrm).where(ArtistOrm.id == artist_id)
                .values(
                    name=artist.name,
                    image_file_name=image_file_name
                )
            )

            await session.execute(stmt)
            await session.commit()

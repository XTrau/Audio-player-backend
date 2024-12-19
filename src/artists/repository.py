from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload, joinedload

from database import new_session
from artists.schemas import SArtistCreate
from file_manager import save_file, delete_file

from artists.models import ArtistOrm
from tracks.models import TrackOrm


class ArtistsRepository:
    @staticmethod
    async def create_artist(artist: SArtistCreate) -> ArtistOrm:
        async with new_session() as session:
            img_file_name = await save_file(
                artist.image_file, ["jpg", "jpeg", "png"], artist.name
            )
            artist_model = ArtistOrm(name=artist.name, image_file_name=img_file_name)
            session.add(artist_model)
            await session.flush()
            await session.commit()
            return artist_model

    @staticmethod
    async def get_artists(page: int, size: int) -> list[ArtistOrm]:
        async with new_session() as session:
            query = select(ArtistOrm).limit(size).offset(page * size)
            res = await session.execute(query)
            artist_models = res.unique().scalars().all()
            return artist_models

    @staticmethod
    async def search_artists(query: str, threshold: float) -> list[ArtistOrm]:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .filter(func.similarity(ArtistOrm.name, query) > threshold)
                .limit(10)
                .order_by(func.similarity(ArtistOrm.name, query).desc())
            )
            result = await session.execute(query)
            artist_models = result.unique().scalars().all()
            return artist_models

    @staticmethod
    async def get_artist(artist_id: int) -> ArtistOrm:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .options(
                    selectinload(ArtistOrm.albums),
                    selectinload(ArtistOrm.tracks).options(
                        selectinload(TrackOrm.artists), joinedload(TrackOrm.album)
                    ),
                )
                .where(ArtistOrm.id == artist_id)
            )
            res = await session.execute(query)
            artist_model = res.unique().scalar()
            return artist_model

    @staticmethod
    async def update_artist(artist_id: int, artist: SArtistCreate) -> ArtistOrm:
        async with new_session() as session:
            query = select(ArtistOrm.image_file_name).where(ArtistOrm.id == artist_id)
            old_image_file_name = (await session.execute(query)).scalar()
            await delete_file(old_image_file_name)

            image_file_name = await save_file(
                artist.image_file, ["jpg", "jpeg", "png"], artist.name
            )
            stmt = (
                update(ArtistOrm)
                .where(ArtistOrm.id == artist_id)
                .values(name=artist.name, image_file_name=image_file_name)
                .returning(ArtistOrm)
            )

            updated_artist = await session.execute(stmt)
            await session.commit()
            return updated_artist.scalar()

    @staticmethod
    async def check_artist(artist_id: int) -> bool:
        async with new_session() as session:
            query = select(ArtistOrm).where(ArtistOrm.id == artist_id)
            artist_model = (await session.execute(query)).scalar()
        return False if not artist_model else True

    @staticmethod
    async def check_artists(artist_ids: list[int]) -> bool:
        async with new_session() as session:
            for artist_id in artist_ids:
                query = select(ArtistOrm).where(ArtistOrm.id == artist_id)
                artist_model = (await session.execute(query)).scalar()
                if not artist_model:
                    return False
        return True

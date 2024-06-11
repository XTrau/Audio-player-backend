from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database import new_session
from src.models import ArtistOrm
from src.schemas import SArtistAdd
from src.file_manager import save_file


class ArtistsRepository:

    @staticmethod
    async def create_artist(artist: SArtistAdd) -> int:
        async with new_session() as session:
            img_file_name = save_file(artist.image_file, ['jpg', 'jpeg', 'png'])
            artist_model = ArtistOrm(name=artist.name, image_file_name=img_file_name)
            session.add(artist_model)
            await session.flush()
            await session.commit()
            return artist_model.id

    @staticmethod
    async def get_artists() -> list[ArtistOrm]:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .options(selectinload(ArtistOrm.albums))
            )
            res = await session.execute(query)
            artists = res.unique().scalars().all()
            return artists

    @staticmethod
    async def get_artist(artist_id: int) -> ArtistOrm | None:
        async with new_session() as session:
            query = (
                select(ArtistOrm)
                .options(selectinload(ArtistOrm.albums))
                .where(ArtistOrm.id == artist_id)
            )
            res = await session.execute(query)
            artist = res.unique().scalars().first()
            return artist
from database import new_session
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload, selectinload

from file_manager import save_file, delete_file

from models import ArtistAlbumOrm
from albums.models import AlbumOrm
from tracks.models import TrackOrm

from albums.schemas import SAlbumCreate

from datetime import datetime


class AlbumsRepository:
    @staticmethod
    async def create_album(album: SAlbumCreate) -> AlbumOrm:
        async with new_session() as session:
            image_file_name = await save_file(
                album.image_file, ["jpg", "jpeg", "png"], album.title
            )
            album_model = AlbumOrm(
                title=album.title,
                image_file_name=image_file_name,
                released_at=album.released_at,
            )

            session.add(album_model)
            await session.flush()
            await session.commit()
            album_model.track_count = 0
            return album_model

    @staticmethod
    async def set_artists(album_id: int, artist_ids: list[int]) -> None:
        async with new_session() as session:
            stmt = delete(ArtistAlbumOrm).where(ArtistAlbumOrm.album_id == album_id)
            await session.execute(stmt)

            for artist_id in artist_ids:
                artist_album_relation_model = ArtistAlbumOrm(
                    artist_id=artist_id, album_id=album_id
                )
                session.add(artist_album_relation_model)

            await session.flush()
            await session.commit()

    @staticmethod
    async def get_albums(page: int, size: int) -> list[AlbumOrm]:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .where(AlbumOrm.released_at <= datetime.utcnow())
                .options(selectinload(AlbumOrm.artists))
                .limit(size)
                .offset(page * size)
            )
            res = await session.execute(query)
            album_models = res.unique().scalars().all()
            return album_models

    @staticmethod
    async def get_album(album_id: int) -> AlbumOrm:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .where(
                    AlbumOrm.id == album_id
                    and AlbumOrm.released_at <= datetime.utcnow()
                )
                .options(
                    selectinload(AlbumOrm.artists),
                    joinedload(AlbumOrm.tracks).options(selectinload(TrackOrm.artists)),
                )
            )
            res = await session.execute(query)
            album_model = res.unique().scalars().first()
            return album_model

    @staticmethod
    async def search_albums(query: str, threshold: float) -> list[AlbumOrm]:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .where(AlbumOrm.released_at <= datetime.utcnow())
                .filter(func.similarity(AlbumOrm.title, query) > threshold)
                .limit(10)
                .options(
                    selectinload(AlbumOrm.artists),
                )
                .order_by(func.similarity(AlbumOrm.title, query).desc())
            )
            result = await session.execute(query)
            album_models = result.unique().scalars().all()
            return album_models

    @staticmethod
    async def update_album(album_id: int, album: SAlbumCreate) -> AlbumOrm:
        async with new_session() as session:
            image_file_name = await save_file(
                album.image_file, ["jpg", "jpeg", "png"], album.title
            )

            query = select(AlbumOrm.image_file_name).where(AlbumOrm.id == album_id)
            old_image_file_name = (await session.execute(query)).scalar()
            await delete_file(old_image_file_name)

            stmt = (
                update(AlbumOrm)
                .where(AlbumOrm.id == album_id)
                .values(
                    title=album.title,
                    image_file_name=image_file_name,
                )
                .returning(AlbumOrm)
            )

            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @staticmethod
    async def check_album(album_id: int):
        async with new_session() as session:
            query = select(AlbumOrm).where(AlbumOrm.id == album_id)
            album_model = (await session.execute(query)).scalar()
        return True if album_model else False

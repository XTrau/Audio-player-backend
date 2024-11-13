from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from artists.models import ArtistOrm
from database import new_session
from models import ArtistAlbumOrm
from albums.schemas import SAlbumCreate
from file_manager import save_file, delete_file

from albums.models import AlbumOrm
from tracks.models import TrackOrm


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
            return album_model

    @staticmethod
    async def check_artists(artist_ids: list[int]) -> bool:
        async with new_session() as session:
            for artist_id in artist_ids:
                query = select(ArtistOrm).where(ArtistOrm.id == artist_id)
                artist_model = await session.execute(query)
                if artist_model is None:
                    return False
            return True

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
                .where(AlbumOrm.released_at <= datetime.utcnow())
                .options(
                    selectinload(AlbumOrm.artists),
                    selectinload(AlbumOrm.tracks).selectinload(TrackOrm.artists),
                )
                .where(AlbumOrm.id == album_id)
            )
            res = await session.execute(query)
            album_models = res.unique().scalars().first()
            return album_models

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
            query = select(AlbumOrm).where(AlbumOrm.id == album_id)

            res = await session.execute(query)
            old_album = res.scalar()
            if old_album is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден"
                )

            await delete_file(old_album.image_file_name)

            image_file_name = await save_file(
                album.image_file, ["jpg", "jpeg", "png"], album.title
            )
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

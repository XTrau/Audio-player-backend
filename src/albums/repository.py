from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from src.database import new_session
from src.schemas import SAlbumAdd
from src.file_manager import save_file, delete_file

from src.albums.models import AlbumOrm
from src.tracks.models import TrackOrm


class AlbumsRepository:
    @staticmethod
    async def create_album(album: SAlbumAdd) -> int:
        async with new_session() as session:
            image_file_name = await save_file(album.image_file, ['jpg', 'jpeg', 'png'], album.title)
            album_model = AlbumOrm(
                title=album.title,
                artist_id=album.artist_id,
                image_file_name=image_file_name
            )
            session.add(album_model)
            await session.flush()
            await session.commit()
            return album_model.id

    @staticmethod
    async def get_albums(page: int, size: int) -> list[AlbumOrm]:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .options(
                    joinedload(AlbumOrm.artist),
                    selectinload(AlbumOrm.tracks).selectinload(TrackOrm.artists)
                )
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
                .options(
                    joinedload(AlbumOrm.artist),
                    selectinload(AlbumOrm.tracks).selectinload(TrackOrm.artists)
                )
                .where(AlbumOrm.id == album_id)
            )
            res = await session.execute(query)
            album_models = res.unique().scalars().first()
            return album_models

    @staticmethod
    async def update_album(
            album_id: int,
            album: SAlbumAdd
    ):
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .where(AlbumOrm.id == album_id)
            )

            res = await session.execute(query)
            old_album = res.scalar()
            if old_album is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Album not found')

            await delete_file(old_album.image_file_name)

            image_file_name = await save_file(album.image_file, ['jpg', 'jpeg', 'png'], album.title)
            stmt = (
                update(AlbumOrm).where(AlbumOrm.id == album_id)
                .values(title=album.title, artist_id=album.artist_id, image_file_name=image_file_name)
            )

            await session.execute(stmt)
            await session.commit()

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.database import new_session
from src.schemas import SAlbumAdd
from src.models import AlbumOrm
from src.file_manager import save_file


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
    async def get_albums() -> list[AlbumOrm]:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .options(joinedload(AlbumOrm.artist))
            )
            res = await session.execute(query)
            album_models = res.unique().scalars().all()
            return album_models

    @staticmethod
    async def get_album(album_id: int) -> AlbumOrm:
        async with new_session() as session:
            query = (
                select(AlbumOrm)
                .options(joinedload(AlbumOrm.artist))
                .where(AlbumOrm.id == album_id)
            )
            res = await session.execute(query)
            album_models = res.unique().scalars().first()
            return album_models

from fastapi import APIRouter, Form, UploadFile, File, Depends, status, HTTPException
from src.albums.repository import AlbumsRepository
from src.schemas import SAlbumAdd, SAlbumWithArtist

router = APIRouter(prefix='/albums', tags=['Albums'])


async def get_artist_create_schema(
        title: str = Form(),
        artist_id: int = Form(),
        image_file: UploadFile = File(None)
):
    return SAlbumAdd(title=title, artist_id=artist_id, image_file=image_file)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_album(
        album: SAlbumAdd = Depends(get_artist_create_schema)
):
    album_id = await AlbumsRepository.create_album(album)
    return {"ok": True, "album_id": album_id}


@router.get('/')
async def get_albums() -> list[SAlbumWithArtist]:
    album_models = await AlbumsRepository.get_albums()
    album_schemas = [SAlbumWithArtist.from_orm(album_model) for album_model in album_models]
    return album_schemas


@router.get('/{artist_id}')
async def get_album(album_id: int) -> SAlbumWithArtist | None:
    album_model = await AlbumsRepository.get_album(album_id)
    if album_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    album_schema = SAlbumWithArtist.from_orm(album_model)
    return album_schema

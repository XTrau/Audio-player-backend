from fastapi import APIRouter, Form, UploadFile, File, Depends, status, HTTPException, Query
from src.albums.repository import AlbumsRepository
from src.schemas import SAlbumAdd, SAlbum

router = APIRouter(prefix='/albums', tags=['Albums'])


async def get_album_create_schema(
        title: str = Form(),
        artist_id: int = Form(),
        image_file: UploadFile = File(None)
):
    return SAlbumAdd(title=title, artist_id=artist_id, image_file=image_file)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_album(
        album: SAlbumAdd = Depends(get_album_create_schema)
):
    album_id = await AlbumsRepository.create_album(album)
    return {"ok": True, "album_id": album_id}


@router.get('/', response_model=list[SAlbum])
async def get_albums(
        page: int = Query(0, ge=0),
        size: int = Query(10, ge=1, le=20),
):
    album_models = await AlbumsRepository.get_albums(page, size)
    album_schemas = [SAlbum.from_orm(album_model) for album_model in album_models]
    return album_schemas


@router.get('/{album_id}', response_model=SAlbum)
async def get_album(album_id: int):
    album_model = await AlbumsRepository.get_album(album_id)
    if album_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    album_schema = SAlbum.from_orm(album_model)
    return album_schema


@router.put('/{album_id}', response_model=SAlbum)
async def update_album(
        album_id: int,
        album: SAlbumAdd = Depends(get_album_create_schema)
):
    await AlbumsRepository.update_album(album_id, album)
    album_model = await AlbumsRepository.get_album(album_id)
    if album_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    album_schema = SAlbum.from_orm(album_model)
    return album_schema

from datetime import datetime

from fastapi import (
    APIRouter,
    Form,
    UploadFile,
    File,
    Depends,
    status,
    HTTPException,
    Query,
)

from albums.repository import AlbumsRepository
from albums.schemas import SAlbumCreate, SAlbumWithArtists, SAlbum
from auth.auth import get_current_administrator_user
from auth.schemas import SUserInDB
from schemas import SAlbumFullInfo

router = APIRouter(tags=["Albums"])


async def get_album_create_schema(
    title: str = Form(),
    artist_ids: list[int] = Form(),
    date_of_release: datetime = Form(default_factory=datetime.utcnow),
    image_file: UploadFile | None = File(default=None),
) -> SAlbumCreate:
    return SAlbumCreate(
        title=title,
        artist_ids=artist_ids,
        image_file=image_file,
        released_at=date_of_release,
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SAlbum)
async def create_album(
    album: SAlbumCreate = Depends(get_album_create_schema),
    admin: SUserInDB = Depends(get_current_administrator_user),
) -> SAlbum:
    artist_check = await AlbumsRepository.check_artists(album.artist_ids)
    if not artist_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Указанных артистов не существует",
        )

    album_model = await AlbumsRepository.create_album(album)
    await AlbumsRepository.set_artists(album_model.id, album.artist_ids)
    album_schema = SAlbum.model_validate(album_model, from_attributes=True)
    return album_schema


@router.get("/", response_model=list[SAlbumWithArtists], status_code=status.HTTP_200_OK)
async def get_albums(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=20),
) -> list[SAlbumWithArtists]:
    album_models = await AlbumsRepository.get_albums(page, size)
    album_schemas = [
        SAlbumWithArtists.model_validate(album_model, from_attributes=True)
        for album_model in album_models
    ]
    return album_schemas


@router.get(
    "/search", response_model=list[SAlbumWithArtists], status_code=status.HTTP_200_OK
)
async def search_album(query: str, threshold: float = 0.4) -> list[SAlbumWithArtists]:
    album_models = await AlbumsRepository.search_albums(query, threshold)
    album_schemas = [
        SAlbumWithArtists.model_validate(album_model, from_attributes=True)
        for album_model in album_models
    ]
    return album_schemas


@router.get("/{album_id}", response_model=SAlbumFullInfo, status_code=status.HTTP_200_OK)
async def get_album(album_id: int) -> SAlbumFullInfo:
    album_model = await AlbumsRepository.get_album(album_id)
    if album_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден"
        )
    album_schema = SAlbumFullInfo.model_validate(album_model, from_attributes=True)
    return album_schema


@router.put("/{album_id}", response_model=SAlbum, status_code=status.HTTP_201_CREATED)
async def update_album(
    album_id: int,
    album: SAlbumCreate = Depends(get_album_create_schema),
    admin: SUserInDB = Depends(get_current_administrator_user),
) -> SAlbum:
    artist_check = await AlbumsRepository.check_artists(album.artist_ids)
    if not artist_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Указанных артистов не существует",
        )

    album_model = await AlbumsRepository.update_album(album_id, album)
    if album_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Альбом не найден"
        )
    await AlbumsRepository.set_artists(album_id, album.artist_ids)
    album_schema = SAlbum.model_validate(album_model, from_attributes=True)
    return album_schema

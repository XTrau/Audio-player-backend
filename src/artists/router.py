from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File,
    status,
    Query,
)

from artists.exceptions import artist_not_found_exception
from artists.models import ArtistOrm
from artists.repository import ArtistsRepository
from artists.schemas import SArtistCreate, SArtist
from schemas import SArtistFullInfo

from auth.auth import get_current_administrator_user
from auth.schemas import SUserInDB

router = APIRouter(tags=["Artists"])


async def get_artist_create_schema(
    name: str = Form(),
    image_file: UploadFile | None = File(default=None),
) -> SArtistCreate:
    return SArtistCreate(name=name, image_file=image_file)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SArtist)
async def create_artist(
    artist: SArtistCreate = Depends(get_artist_create_schema),
    admin: SUserInDB = Depends(get_current_administrator_user),
) -> SArtist:
    artist_model: ArtistOrm = await ArtistsRepository.create_artist(artist)
    artist_schema: SArtist = SArtist.model_validate(artist_model, from_attributes=True)
    return artist_schema


@router.get("/", response_model=list[SArtist])
async def get_artists(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=20),
) -> list[SArtist]:
    artist_models: list[ArtistOrm] = await ArtistsRepository.get_artists(page, size)
    artist_schemas: list[SArtist] = [
        SArtist.model_validate(artist_model, from_attributes=True)
        for artist_model in artist_models
    ]
    return artist_schemas


@router.get("/search", response_model=list[SArtist])
async def search_artists(query: str, threshold: float = 0.4) -> list[SArtist]:
    artist_models: list[ArtistOrm] = await ArtistsRepository.search_artists(
        query=query, threshold=threshold
    )
    artist_schemas: list[SArtist] = [
        SArtist.model_validate(artist_model, from_attributes=True)
        for artist_model in artist_models
    ]
    return artist_schemas


@router.get("/{artist_id}", response_model=SArtistFullInfo)
async def get_artist(artist_id: int) -> SArtistFullInfo:
    artist_model: ArtistOrm | None = await ArtistsRepository.get_artist(artist_id)
    if artist_model is None:
        raise artist_not_found_exception

    artist_schema: SArtistFullInfo = SArtistFullInfo.model_validate(
        artist_model, from_attributes=True
    )
    return artist_schema


@router.put("/{artist_id}", response_model=SArtist)
async def update_artist(
    artist_id: int,
    artist: SArtistCreate = Depends(get_artist_create_schema),
    admin: SUserInDB = Depends(get_current_administrator_user),
) -> SArtist:
    check_artist: bool = await ArtistsRepository.check_artist(artist_id)
    if not check_artist:
        raise artist_not_found_exception

    updated_artist: ArtistOrm = await ArtistsRepository.update_artist(artist_id, artist)
    artist_schema: SArtist = SArtist.model_validate(
        updated_artist, from_attributes=True
    )
    return artist_schema

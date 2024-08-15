from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File,
    HTTPException,
    status,
    Query,
)
from artists.repository import ArtistsRepository
from schemas import SArtistAdd, SArtist

router = APIRouter(prefix="/artists", tags=["Artists"])


async def get_artist_create_schema(
        name: str = Form(),
        image_file: Optional[UploadFile] = File(default=None),
) -> SArtistAdd:
    return SArtistAdd(name=name, image_file=image_file)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artist(artist: SArtistAdd = Depends(get_artist_create_schema)):
    artist_id = await ArtistsRepository.create_artist(artist)
    return {"ok": True, "artist_id": artist_id}


@router.get("/", response_model=list[SArtist])
async def get_artists(
        page: int = Query(0, ge=0),
        size: int = Query(10, ge=1, le=20),
):
    artist_models = await ArtistsRepository.get_artists(page, size)
    artist_schemas = [
        SArtist.model_validate(artist_model, from_attributes=True)
        for artist_model in artist_models
    ]
    return artist_schemas


@router.get("/{artist_id}", response_model=SArtist)
async def get_artist(artist_id: int):
    artist_model = await ArtistsRepository.get_artist(artist_id)
    if artist_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found"
        )
    artist_schema = SArtist.model_validate(artist_model, from_attributes=True)
    return artist_schema


@router.put("/{artist_id}", response_model=SArtist)
async def update_artist(
        artist_id: int,
        artist: SArtistAdd = Depends(get_artist_create_schema),
):
    await ArtistsRepository.update_artist(artist_id, artist)
    artist_model = await ArtistsRepository.get_artist(artist_id)
    if artist_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found"
        )
    artist_schema = SArtist.model_validate(artist_model, from_attributes=True)
    return artist_schema

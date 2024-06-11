from fastapi import APIRouter, Depends, Form, UploadFile, File
from src.artists.repository import ArtistsRepository
from src.schemas import SArtistAdd

router = APIRouter(prefix='/artists', tags=['Artists'])


async def get_artist_create_model(
        name: str = Form(),
        image_file: UploadFile = File(None)
) -> SArtistAdd:
    return SArtistAdd(name=name, image_file=image_file)


@router.post("/")
async def create_artist(artist: SArtistAdd = Depends(get_artist_create_model)):
    artist_id = await ArtistsRepository.create_artist(artist)
    return {"ok": True, "artist_id": artist_id}


@router.get("/")
async def get_artists():
    artists_models = await ArtistsRepository.get_artists()
    return artists_models


@router.get("/{artist_id}")
async def get_artist(artist_id: int):
    artists_models = await ArtistsRepository.get_artist(artist_id)
    return artists_models

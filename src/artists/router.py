from fastapi import APIRouter, Depends, Form, UploadFile, File
from src.artists.repository import ArtistsRepository
from src.schemas import SArtistAdd, SArtistWithAlbums

router = APIRouter(prefix='/artists', tags=['Artists'])


async def get_artist_create_schema(
        name: str = Form(),
        image_file: UploadFile = File(None),
) -> SArtistAdd:
    return SArtistAdd(name=name, image_file=image_file)


@router.post("/")
async def create_artist(artist: SArtistAdd = Depends(get_artist_create_schema)):
    artist_id = await ArtistsRepository.create_artist(artist)
    return {"ok": True, "artist_id": artist_id}


@router.get("/")
async def get_artists() -> list[SArtistWithAlbums]:
    artists_models = await ArtistsRepository.get_artists()
    artist_schemas = [SArtistWithAlbums.from_orm(artists_model) for artists_model in artists_models]
    return artist_schemas


@router.get("/{artist_id}")
async def get_artist(artist_id: int) -> SArtistWithAlbums:
    artist_model = await ArtistsRepository.get_artist(artist_id)
    artist_schema = SArtistWithAlbums.from_orm(artist_model)
    return artist_schema

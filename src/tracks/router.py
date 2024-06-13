from fastapi import APIRouter, Form, File, UploadFile, Depends, status, Body
from src.schemas import STrack, STrackAdd, STrackWithAlbum
from src.tracks.repository import TracksRepository

router = APIRouter(prefix='/tracks', tags=['Tracks'])


async def get_artist_ids(
        artist_ids: str = Form(description="Input (str): 1,2,3,4")
):
    artist_ids_list = list(map(int, artist_ids.split(',')))
    return artist_ids_list


async def get_track_create_schema(
        title: str = Form(),
        artist_ids: list[int] = Depends(get_artist_ids),
        album_id: int | None = Form(None),
        audio_file: UploadFile = File(),
        image_file: UploadFile = File(None)
):
    return STrackAdd(
        title=title,
        artist_ids=artist_ids,
        album_id=album_id,
        audio_file=audio_file,
        image_file=image_file
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_track(track: STrackAdd = Depends(get_track_create_schema)):
    track_id = await TracksRepository.create_track(track)
    return {"ok": True, "track_id": track_id}


@router.get("/")
async def get_tracks() -> list[STrackWithAlbum]:
    track_models = await TracksRepository.get_tracks()
    track_schemas = [STrackWithAlbum.from_orm(track_model) for track_model in track_models]
    return track_schemas


@router.get("/{track_id}")
async def get_track(track_id: int) -> STrackWithAlbum:
    track_model = await TracksRepository.get_track(track_id)
    track_schema = STrackWithAlbum.from_orm(track_model)
    return track_schema

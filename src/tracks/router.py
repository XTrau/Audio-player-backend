from fastapi import (
    APIRouter,
    Form,
    File,
    UploadFile,
    Depends,
    status,
    Query,
    HTTPException,
)
from schemas import STrack, STrackAdd
from tracks.repository import TracksRepository

router = APIRouter(prefix="/tracks", tags=["Tracks"])


async def get_artist_ids(artist_ids: str = Form(description="Input (str): 1,2,3,4")):
    artist_ids_list = list(map(int, artist_ids.split(",")))
    return artist_ids_list


async def get_track_create_schema(
    title: str = Form(),
    artist_ids: list[int] = Depends(get_artist_ids),
    album_id: int | None = Form(None),
    audio_file: UploadFile = File(),
    image_file: UploadFile = File(None),
):
    return STrackAdd(
        title=title,
        artist_ids=artist_ids,
        album_id=album_id,
        audio_file=audio_file,
        image_file=image_file,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_track(track: STrackAdd = Depends(get_track_create_schema)):
    track_id = await TracksRepository.create_track(track)
    return {"ok": True, "track_id": track_id}


@router.get("/", response_model=list[STrack])
async def get_tracks(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=20),
):
    track_models = await TracksRepository.get_tracks(page, size)
    track_schemas = [
        STrack.model_validate(track_model, from_attributes=True)
        for track_model in track_models
    ]
    return track_schemas


@router.get("/{track_id}", response_model=STrack)
async def get_track(track_id: int):
    track_model = await TracksRepository.get_track(track_id)
    if track_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Track not found"
        )
    track_schema = STrack.model_validate(track_model, from_attributes=True)
    return track_schema


@router.put("/{track_id}", response_model=STrack)
async def update_track(
    track_id: int, track: STrackAdd = Depends(get_track_create_schema)
):
    await TracksRepository.update_track(track_id, track)
    track_model = await TracksRepository.get_track(track_id)
    if track_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Track not found"
        )
    track_schema = STrack.model_validate(track_model, from_attributes=True)
    return track_schema

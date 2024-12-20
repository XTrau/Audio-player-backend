from fastapi import (
    APIRouter,
    Form,
    File,
    UploadFile,
    Depends,
    status,
    Query,
)

from artists.exceptions import artist_not_found_exception
from artists.repository import ArtistsRepository
from auth.auth import get_current_administrator_user
from auth.schemas import SUserInDB
from playlist.repository import track_not_found_exception
from schemas import STrackFullInfo
from tracks.models import TrackOrm
from tracks.schemas import STrack, STrackCreate
from tracks.repository import TracksRepository

router = APIRouter(tags=["Tracks"])


async def get_track_create_schema(
    title: str = Form(),
    artist_ids: list[int] = Form(),
    album_id: int = Form(),
    number_at_album: int = Form(),
    audio_file: UploadFile = File(),
    image_file: UploadFile | None = File(None),
):
    return STrackCreate(
        title=title,
        artist_ids=artist_ids,
        album_id=album_id,
        audio_file=audio_file,
        image_file=image_file,
        number_at_album=number_at_album,
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=STrack)
async def create_track(
    track: STrackCreate = Depends(get_track_create_schema),
    admin: SUserInDB = Depends(get_current_administrator_user),
):
    check_artists = await ArtistsRepository.check_artists(track.artist_ids)
    if not check_artists:
        raise artist_not_found_exception
    track_model = await TracksRepository.create_track(track)
    await TracksRepository.set_artists(track_model.id, track.artist_ids)
    return STrack.model_validate(track_model, from_attributes=True)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[STrackFullInfo])
async def get_tracks(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=20),
) -> list[STrackFullInfo]:
    track_models = await TracksRepository.get_tracks(page, size)
    track_schemas = [
        STrackFullInfo.model_validate(track_model, from_attributes=True)
        for track_model in track_models
    ]
    return track_schemas


@router.get(
    "/{track_id}", response_model=STrackFullInfo, status_code=status.HTTP_200_OK
)
async def get_track(track_id: int) -> STrackFullInfo:
    track_model = await TracksRepository.get_track(track_id)
    if track_model is None:
        raise track_not_found_exception
    track_schema = STrackFullInfo.model_validate(track_model, from_attributes=True)
    return track_schema


@router.put("/{track_id}", response_model=STrack)
async def update_track(
    track_id: int, track: STrackCreate = Depends(get_track_create_schema)
):
    check_artists: bool = await ArtistsRepository.check_artists(track.artist_ids)
    if not check_artists:
        raise artist_not_found_exception

    await TracksRepository.update_track(track_id, track)
    track_model: TrackOrm = await TracksRepository.get_track(track_id)
    if track_model is None:
        raise track_not_found_exception
    track_schema: STrack = STrack.model_validate(track_model, from_attributes=True)
    return track_schema


@router.delete("/{track_id}", response_model=STrack, status_code=status.HTTP_200_OK)
async def delete_track(
    track_id: int,
    admin: SUserInDB = Depends(get_current_administrator_user),
):
    check_track: bool = await TracksRepository.check_track(track_id)
    if not check_track:
        raise track_not_found_exception

    track: TrackOrm = await TracksRepository.delete_track(track_id)
    return track

from fastapi import APIRouter, status, Depends, HTTPException

from auth.auth import get_current_user
from auth.schemas import SUserInDB
from schemas import STrackFullInfo
from liked_tracks.repository import UserLikesRepository
from tracks.repository import TracksRepository

router = APIRouter(tags=["Liked Tracks"])


# Liked_tracks
@router.post(
    path="/like_track", status_code=status.HTTP_201_CREATED, response_model=None
)
async def like_track(
    track_id: int, user: SUserInDB = Depends(get_current_user)
) -> None:
    if not TracksRepository.check_track(track_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Указанный трек не найден"
        )
    await UserLikesRepository.like_track(user.id, track_id)


@router.post(path="/unlike_track", status_code=status.HTTP_200_OK, response_model=None)
async def unlike_track(
    track_id: int,
    user: SUserInDB = Depends(get_current_user)
) -> None:
    await UserLikesRepository.unlike_track(user.id, track_id)


@router.get(
    path="/me/liked",
    status_code=status.HTTP_200_OK,
    response_model=list[STrackFullInfo],
)
async def get_liked_tracks(
    user: SUserInDB = Depends(get_current_user),
) -> list[STrackFullInfo]:
    track_models = await UserLikesRepository.get_liked_tracks(user.id)
    track_schemas = [
        STrackFullInfo.model_validate(track_model, from_attributes=True)
        for track_model in track_models
    ]
    return track_schemas


@router.get(
    path="/me/liked_ids",
    status_code=status.HTTP_200_OK,
    response_model=list[int],
)
async def get_liked_track_ids(
    user: SUserInDB = Depends(get_current_user),
) -> list[int]:
    liked_ids: list[int] = await UserLikesRepository.get_liked_track_ids(user.id)
    return liked_ids

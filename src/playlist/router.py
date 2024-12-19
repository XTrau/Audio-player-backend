from fastapi import APIRouter, Form, Depends

from auth.auth import get_current_user
from auth.schemas import SUserInDB
from playlist.models import PlaylistOrm
from playlist.repository import PlaylistRepository
from playlist.schemas import SPlaylistCreate

router = APIRouter(tags=["Playlists"])


@router.post("/")
async def create_playlist(
    new_playlist: SPlaylistCreate = Form(),
    user: SUserInDB = Depends(get_current_user)
):
    playlist_model = PlaylistRepository.create_playlist(new_playlist, user.id)
    pass


@router.get("/{playlist_id}")
async def get_playlist(
    new_playlist: SPlaylistCreate = Form(),
    user: SUserInDB = Depends(get_current_user)
):
    playlist_model: PlaylistOrm = await PlaylistRepository.create_playlist(new_playlist, user.id)
    pass
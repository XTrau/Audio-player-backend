from fastapi import APIRouter

from playlist.models import PlaylistOrm

router = APIRouter(tags=["Playlists"])

@router.get("/")
async def playlist():
    a = PlaylistOrm()
    return "123"
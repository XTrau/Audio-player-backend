from fastapi import UploadFile, File
from pydantic import BaseModel


class SAlbumAdd(BaseModel):
    title: str
    artist_id: int
    image_file: UploadFile | None = File(None)


class SAlbumBase(BaseModel):
    id: int
    title: str
    image_file_name: str | None = None
    artist_id: int


class SAlbum(SAlbumBase):
    artist: "SArtistBase" | None = None
    tracks: list["STrackBase"]

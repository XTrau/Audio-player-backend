from fastapi import UploadFile, File
from pydantic import BaseModel


class STrackAdd(BaseModel):
    title: str
    album_id: int | None = None
    artist_ids: list[int]
    audio_file: UploadFile
    image_file: UploadFile | None = File(None)


class STrackBase(BaseModel):
    id: int
    title: str
    audio_file_name: str
    image_file_name: str | None = None

    artists: list["SArtistBase"]


class STrack(STrackBase):
    album: "SAlbumBase" | None = None

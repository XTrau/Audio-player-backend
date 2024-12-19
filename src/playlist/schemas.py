from fastapi import UploadFile
from pydantic import BaseModel


class SPlaylistCreate(BaseModel):
    title: str
    image_file: UploadFile
    track_ids: list[int]


class SPlaylist(BaseModel):
    title: str
    image_file: UploadFile
    pass

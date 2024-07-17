from fastapi import UploadFile, File
from pydantic import BaseModel


class SArtistAdd(BaseModel):
    name: str
    image_file: UploadFile | None = File(None)


class SArtistBase(BaseModel):
    id: int
    name: str
    image_file_name: str | None = None


class SArtist(SArtistBase):
    albums: list["SAlbumBase"]
    tracks: list["STrack"]

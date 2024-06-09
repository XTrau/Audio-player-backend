from fastapi import UploadFile
from pydantic import BaseModel


class ArtistCreateModel(BaseModel):
    name: str
    image_file: UploadFile | None = None


class TrackCreateModel(BaseModel):
    title: str
    audio_file: UploadFile
    image_file: UploadFile | None = None


class AlbumCreateModel(BaseModel):
    title: str
    image_file: UploadFile | None = None

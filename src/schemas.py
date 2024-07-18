from fastapi import UploadFile, File
from pydantic import BaseModel, BaseConfig


class SArtistAdd(BaseModel):
    name: str
    image_file: UploadFile | None = File(None)


class SAlbumAdd(BaseModel):
    title: str
    artist_id: int
    image_file: UploadFile | None = File(None)


class STrackAdd(BaseModel):
    title: str
    album_id: int | None = None
    artist_ids: list[int]
    audio_file: UploadFile
    image_file: UploadFile | None = File(None)


class SArtistBase(BaseModel):
    id: int
    name: str
    image_file_name: str | None = None

    class Config(BaseConfig):
        from_attributes = True


class SAlbumBase(BaseModel):
    id: int
    title: str
    image_file_name: str | None = None
    artist_id: int

    class Config(BaseConfig):
        from_attributes = True


class STrackBase(BaseModel):
    id: int
    title: str
    audio_file_name: str
    image_file_name: str | None = None

    artists: list[SArtistBase]

    class Config(BaseConfig):
        from_attributes = True


class STrack(STrackBase):
    album: SAlbumBase | None = None


class SArtist(SArtistBase):
    albums: list[SAlbumBase]
    tracks: list[STrack]


class SAlbum(SAlbumBase):
    artist: SArtistBase | None = None
    tracks: list[STrackBase]

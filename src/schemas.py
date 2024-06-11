from fastapi import UploadFile, File
from pydantic import BaseModel, BaseConfig


class SArtistAdd(BaseModel):
    name: str
    image_file: UploadFile | None = File(None)


class STrackAdd(BaseModel):
    title: str
    album_id: int | None = None
    artist_ids: list[int]
    audio_file: UploadFile
    image_file: UploadFile | None = File(None)


class SAlbumAdd(BaseModel):
    title: str
    artist_id: int
    image_file: UploadFile | None = File(None)


class SAlbumWithTracksAdd(SAlbumAdd):
    tracks: list[STrackAdd]


class SArtist(BaseModel):
    id: int
    name: str
    image_file_name: str | None = None

    class Config(BaseConfig):
        from_attributes = True


class SAlbum(BaseModel):
    id: int
    title: str
    image_file_name: str | None = None
    artist_id: int

    class Config(BaseConfig):
        from_attributes = True


class STrack(BaseModel):
    id: int
    title: str
    audio_file_name: str
    image_file_name: str | None = None
    artists: list[SArtist]

    class Config(BaseConfig):
        from_attributes = True


class SAlbumWithTracks(SAlbum):
    tracks: list[STrack]


class SAlbumWithArtist(SAlbum):
    artist: SArtist


class SAlbumWithArtistAndTracks(SAlbum):
    artist: SArtist
    tracks: list[STrack]


class SArtistWithAlbums(SArtist):
    albums: list[SAlbum]


class SArtistWithAlbumsAndTracks(SArtist):
    albums: list[SAlbumWithTracks]

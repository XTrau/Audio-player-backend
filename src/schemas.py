from fastapi import UploadFile, File
from pydantic import BaseModel


class SArtistAdd(BaseModel):
    name: str
    image_file: UploadFile | None = File(None)


class STrackAdd(BaseModel):
    title: str
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


class SAlbum(BaseModel):
    title: str
    image_file_name: str | None = None


class STrack(BaseModel):
    title: str
    audio_file_name: str
    image_file_name: str | None = None
    artists: list[SArtist]


class SAlbumWithTracks(SAlbum):
    tracks: list[STrack]


class SArtistWithAlbums(SArtist):
    albums: list[SAlbum]


class SArtistWithAlbumsAndTracks(SArtist):
    albums: list[SAlbumWithTracks]

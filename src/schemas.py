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
    artist_id: int
    image_file: UploadFile | None = None


class AlbumWithTracksCreateModel(AlbumCreateModel):
    tracks: list[TrackCreateModel]


class ArtistModel(BaseModel):
    id: int
    name: str
    image_file_name: str | None = None


class AlbumModel(BaseModel):
    title: str
    image_file_name: str | None = None


class TrackModel(BaseModel):
    title: str
    audio_file_name: str
    image_file_name: str | None = None
    artists: list[ArtistModel]


class AlbumWithTracksModel(AlbumModel):
    tracks: list[TrackModel]


class ArtistWithAlbumsModel(ArtistModel):
    albums: list[AlbumModel]


class ArtistWithAlbumsAndTracksModel(ArtistModel):
    albums: list[AlbumWithTracksModel]

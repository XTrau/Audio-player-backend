from pydantic import BaseModel


class ArtistCreateModel(BaseModel):
    name: str
    image_file_name: str | None = None


class AlbumCreateModel(BaseModel):
    title: str
    image_file_name: str | None = None


class TrackCreateModel(BaseModel):
    title: str
    image_file_name: str | None = None
    audio_file_name: str

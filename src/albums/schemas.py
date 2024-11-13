from datetime import datetime
import re

from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel, field_validator, Field

from artists.schemas import SArtist


class SAlbumCreate(BaseModel):
    title: str
    artist_ids: list[int]
    released_at: datetime = Field(default_factory=datetime.utcnow)
    image_file: UploadFile | None = File(None)

    @field_validator("title")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not (3 <= len(value) <= 64):
            raise HTTPException(
                status_code=422,
                detail="Название альбома должно быть длинной от 3 до 64 символов.",
            )
        regex = r"^[A-Za-zА-Яа-яЁё0-9\s'$-]{3,64}$"
        if not re.match(regex, value):
            raise HTTPException(
                status_code=422,
                detail="Название альбома может содержать только буквы русского и английского алфавитов, пробелы, дефисы и апострофы, и быть длиной от 3 до 64 символов.",
            )
        return value


class SAlbum(BaseModel):
    id: int
    title: str
    image_file_name: str | None
    released_at: datetime

class SAlbumWithArtists(SAlbum):
    artists: list[SArtist]

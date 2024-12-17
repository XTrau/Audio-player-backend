from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel, field_validator
import re


class STrackCreate(BaseModel):
    title: str
    artist_ids: list[int]

    audio_file: UploadFile
    image_file: UploadFile | None = File(None)

    album_id: int
    number_at_album: int

    @field_validator("title")
    @classmethod
    def check_title(cls, value):
        if not (3 <= len(value) <= 256):
            raise HTTPException(
                status_code=422,
                detail="Название трека должно быть длиной от 3 до 256 символов.",
            )
        return value


class STrack(BaseModel):
    id: int
    title: str

    audio_file_name: str
    image_file_name: str | None = None

    number_at_album: int

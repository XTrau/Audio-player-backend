import re

from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel, field_validator


class SArtistCreate(BaseModel):
    name: str
    image_file: UploadFile | None = File(None)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not (3 <= len(value) <= 255):
            raise HTTPException(
                status_code=422,
                detail="Имя артиста должно быть длиной от 3 до 255 символов.",
            )

        return value


class SArtist(BaseModel):
    id: int
    name: str
    image_file_name: str | None = None

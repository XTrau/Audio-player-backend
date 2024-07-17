from fastapi import UploadFile, File, Query
from pydantic import BaseModel, BaseConfig


class Pagination(BaseModel):
    page: int = Query(0, ge=0)
    size: int = Query(10, ge=1, le=50)

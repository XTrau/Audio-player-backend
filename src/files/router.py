from fastapi import APIRouter, HTTPException
from src.file_manager import UPLOAD_DIRECTORY
from starlette.responses import FileResponse
import os

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{file_name}')
async def read_file(file_name: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='File not found')
    file = FileResponse(file_path)
    return file

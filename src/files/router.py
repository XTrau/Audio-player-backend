from fastapi import APIRouter
from src.file_manager import read_file
from starlette.responses import FileResponse

router = APIRouter(prefix='/files', tags=['Files'])


@router.get('/{file_name}')
async def get_file(file_name: str) -> FileResponse:
    file = await read_file(file_name)
    return FileResponse(file.default)

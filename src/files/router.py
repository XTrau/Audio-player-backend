from fastapi import APIRouter, File
from file_manager import read_file
from starlette.responses import FileResponse

router = APIRouter(tags=["Files"])


@router.get("/{file_name}")
async def get_file(file_name: str) -> FileResponse:
    file: File = await read_file(file_name)
    return FileResponse(file.default)

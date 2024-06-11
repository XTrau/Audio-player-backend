import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def save_file(file: UploadFile | None, extensions: list[str]) -> str | None :
    if file is None:
        return None

    file_extension = file.filename.split(".")[-1] in extensions
    if not file_extension:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_id = str(uuid4())
    file_name = f"{file_id}_{file.filename}"
    file_location = os.path.join(UPLOAD_DIRECTORY, file_name)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    return file_name


def delete_file(file_name: str) -> None:
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

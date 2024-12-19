from fastapi import HTTPException, status

album_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Указанный альбом не найден"
)

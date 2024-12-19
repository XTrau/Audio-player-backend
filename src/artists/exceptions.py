from fastapi import HTTPException, status

artist_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Указанный артист не найден"
)

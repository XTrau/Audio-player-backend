from fastapi import HTTPException, status

unauthorized_user_exception = HTTPException(
    status.HTTP_401_UNAUTHORIZED, detail="Пользователь не прошел авторизацию"
)

user_username_already_exists_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь с таким username уже существует",
)

user_email_already_exists_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Пользователь с таким email уже существует",
)

access_denied_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Отказано в доступе",
)


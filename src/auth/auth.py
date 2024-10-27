from fastapi import Depends, HTTPException, Request, Body
from starlette import status

from jwt import exceptions

from auth.models import UserOrm
from auth.repository import UserRepository, get_user_repository
from auth.schemas import SUserCreate, SUser, SUserInDB, SUserLogin, TokenPair

from auth.jwt import create_token_pair, decode_jwt

from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"])

UNAUTHORIZED_USER_EXCEPTION = HTTPException(
    status.HTTP_401_UNAUTHORIZED, detail="Пользователь неавторизован"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def register_user(
    user: SUserCreate = Body(),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user_in_db_email: UserOrm = await user_repository.find_by_email(user.email)
    user_in_db_username: UserOrm = await user_repository.find_by_username(user.username)
    if user_in_db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь с таким email уже существует",
        )
    if user_in_db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь с таким username уже существует",
        )
    hashed_password = hash_password(user.password)
    user_model = await user_repository.create(user, hashed_password)
    user_schema = SUser.model_validate(user_model, from_attributes=True)
    return user_schema


async def login_user(
    user: SUserLogin = Body(),
    user_repository: UserRepository = Depends(get_user_repository),
) -> TokenPair:
    user_model = await user_repository.find_by_email(user.login)
    if user_model is None:
        user_model = await user_repository.find_by_username(user.login)

    if user_model is None or not check_password(
        user.password, user_model.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильный логин или пароль",
        )

    access_token_payload = {"email": user_model.email}
    refresh_token_payload = {"email": user_model.email}

    return create_token_pair(
        access_token_payload=access_token_payload,
        refresh_token_payload=refresh_token_payload,
    )


async def get_refresh_token(
    request: Request,
) -> str:
    refresh_token = request.cookies.get(settings.jwt.REFRESH_TOKEN_NAME)
    if refresh_token is None:
        raise UNAUTHORIZED_USER_EXCEPTION
    try:
        refresh_token_payload = decode_jwt(token=refresh_token)
    except exceptions.InvalidTokenError or exceptions.ExpiredSignatureError:
        raise UNAUTHORIZED_USER_EXCEPTION
    return refresh_token


async def get_access_token(
    request: Request,
    refresh_token: str = Depends(get_refresh_token),
) -> str:
    access_token: str = request.cookies.get(settings.jwt.ACCESS_TOKEN_NAME)
    if access_token is None:
        raise UNAUTHORIZED_USER_EXCEPTION
    try:
        access_token_payload: dict = decode_jwt(token=access_token)
    except exceptions.InvalidTokenError or exceptions.ExpiredSignatureError:
        raise UNAUTHORIZED_USER_EXCEPTION

    return access_token


async def refresh_token_pair(
    refresh_token: str = Depends(get_refresh_token),
) -> TokenPair:
    refresh_token_payload: dict = decode_jwt(token=refresh_token)
    payload: dict = refresh_token_payload.get("sub")
    email: str = payload.get("email")

    access_token_payload = {"email": email}
    refresh_token_payload = {"email": email}

    return create_token_pair(
        access_token_payload=access_token_payload,
        refresh_token_payload=refresh_token_payload,
    )


async def get_current_user(
    access_token: str = Depends(get_access_token),
    user_repository: UserRepository = Depends(get_user_repository),
) -> SUserInDB:
    access_token_payload: dict = decode_jwt(token=access_token)
    payload: dict = access_token_payload.get("sub")
    email: str = payload.get("email")

    user_model: UserOrm = await user_repository.find_by_email(email)
    return SUserInDB.model_validate(user_model, from_attributes=True)


async def get_current_administrator_user(
    user: SUserInDB = Depends(get_current_user),
) -> SUserInDB:
    if user.is_admin is True:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="У пользователя недостаточно прав",
    )

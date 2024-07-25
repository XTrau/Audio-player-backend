import jwt
from fastapi import Depends, Request, HTTPException, Response, status
from passlib.context import CryptContext

from src.auth.schemas import SUserInDB, SUser
from src.auth.repository import UserRepository
from src.auth.jwt import (
    create_access_token,
    decode_jwt,
)

from jwt.exceptions import ExpiredSignatureError

from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(email: str) -> SUserInDB:
    user_model = await UserRepository.get_user_by_email(email)
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return SUserInDB.model_validate(user_model, from_attributes=True)


async def authenticate_user(email: str, password: str) -> SUser:
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return SUser.model_validate(user, from_attributes=True)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


async def get_refresh_token_data(request: Request) -> dict:
    token = request.cookies.get(settings.jwt.refresh_token_type)
    if token is None:
        raise credentials_exception
    try:
        decoded_data = decode_jwt(token=token)
    except jwt.InvalidTokenError:
        raise credentials_exception
    return decoded_data


async def get_access_token_data(
    response: Response,
    request: Request,
    refresh_token_data: dict = Depends(get_refresh_token_data),
) -> dict:
    async def generate_and_set_access_token() -> str:
        email = refresh_token_data.get("sub")
        if email in None:
            raise credentials_exception
        user = await get_user(email)
        if user is None:
            raise credentials_exception
        token = create_access_token(user)
        response.set_cookie(
            settings.jwt.access_token_type,
            token,
            httponly=True,
            max_age=settings.jwt.access_token_expire_seconds,
        )
        return token

    token = request.cookies.get(settings.jwt.access_token_type)
    if token is None:
        token = await generate_and_set_access_token()

    try:
        payload = decode_jwt(token)
    except jwt.InvalidTokenError as e:
        if isinstance(e, ExpiredSignatureError):
            token = await generate_and_set_access_token()
            return decode_jwt(token)
        raise credentials_exception
    else:
        return payload


async def get_current_user(
    access_token_data: dict = Depends(get_access_token_data),
) -> SUser:
    email = access_token_data.get("sub")
    if email is None:
        raise credentials_exception
    user = await get_user(email)
    if user is None:
        raise credentials_exception
    return SUser.model_validate(user, from_attributes=True)


async def get_current_active_user(
    current_user: SUser = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

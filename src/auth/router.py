from datetime import datetime, UTC

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Response, Depends, status, HTTPException

from auth.auth import register_user, login_user, get_current_user, refresh_token_pair
from auth.schemas import SUserInDB, TokenPair, SUser
from config import settings

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register(
    user: SUserInDB = Depends(register_user),
):
    return user


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(response: Response, token_pair: TokenPair = Depends(login_user)):
    response.set_cookie(
        settings.jwt.ACCESS_TOKEN_NAME,
        token_pair.access_token,
        expires=datetime.now(UTC)
        + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        settings.jwt.REFRESH_TOKEN_NAME,
        token_pair.refresh_token,
        expires=datetime.now(UTC)
        + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key=settings.jwt.ACCESS_TOKEN_NAME)
    response.delete_cookie(key=settings.jwt.REFRESH_TOKEN_NAME)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh_tokens(
    response: Response, new_token_pair: TokenPair = Depends(refresh_token_pair)
):
    response.set_cookie(
        settings.jwt.ACCESS_TOKEN_NAME,
        new_token_pair.access_token,
        expires=datetime.now(UTC)
        + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        settings.jwt.REFRESH_TOKEN_NAME,
        new_token_pair.refresh_token,
        expires=datetime.now(UTC)
        + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=SUser, status_code=status.HTTP_200_OK)
async def get_user(
    user: SUserInDB = Depends(get_current_user),
) -> SUser:
    user_schema: SUser = SUser.model_validate(user, from_attributes=True)
    return user_schema

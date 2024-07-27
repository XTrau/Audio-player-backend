from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.exc import IntegrityError

from auth.repository import UserRepository
from auth.jwt import generate_token_pair
from auth.schemas import SUserCreate, SUser, TokenPair
from auth.auth import get_password_hash, authenticate_user, get_current_user
from config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenPair)
async def register_user(response: Response, user: SUserCreate) -> TokenPair:
    user.hashed_password = get_password_hash(user.password)

    try:
        user_model = await UserRepository.create_user(user)
    except IntegrityError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User already exists")

    user_schema = SUser.model_validate(user_model.__dict__)
    token_pair: TokenPair = generate_token_pair(user_schema)
    response.set_cookie(
        settings.jwt.access_token_type,
        token_pair.access_token,
        httponly=True,
        max_age=settings.jwt.access_token_expire_seconds,
    )
    response.set_cookie(
        settings.jwt.refresh_token_type,
        token_pair.refresh_token,
        httponly=True,
        max_age=settings.jwt.refresh_token_expire_seconds,
    )
    return token_pair


@router.post("/login", response_model=TokenPair)
async def login_user(
    response: Response, user: SUser = Depends(authenticate_user)
) -> TokenPair:
    token_pair: TokenPair = generate_token_pair(user)
    response.set_cookie(
        settings.jwt.access_token_type,
        token_pair.access_token,
        httponly=True,
        max_age=settings.jwt.access_token_expire_seconds,
    )
    response.set_cookie(
        settings.jwt.refresh_token_type,
        token_pair.refresh_token,
        httponly=True,
        max_age=settings.jwt.refresh_token_expire_seconds,
    )
    return token_pair


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(settings.jwt.access_token_type)
    response.delete_cookie(settings.jwt.refresh_token_type)


@router.get("/me", response_model=SUser)
async def get_me(user: SUser = Depends(get_current_user)) -> SUser:
    return user

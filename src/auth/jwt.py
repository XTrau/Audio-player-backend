from datetime import datetime, timedelta, timezone
from os import access

import jwt

from config import settings
from auth.schemas import SUser, TokenPair


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    if expire_timedelta:
        expire = datetime.now(timezone.utc) + expire_timedelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload.update({"exp": expire})
    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> dict:
    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload, expire_timedelta=expire_timedelta)


def create_access_token(user: SUser) -> str:
    jwt_payload = {"sub": user.email, "email": user.email, "username": user.username}
    return create_jwt(
        token_type=settings.jwt.access_token_type,
        token_data=jwt_payload,
    )


def create_refresh_token(user: SUser) -> str:
    jwt_payload = {"sub": user.email}
    return create_jwt(
        token_type=settings.jwt.access_token_type,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.jwt.refresh_token_expire_days),
    )


def generate_token_pair(user: SUser) -> TokenPair:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)

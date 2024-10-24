from datetime import datetime, timedelta, UTC

import jwt

from auth.schemas import TokenPair
from config import settings


def decode_jwt(
        token: str,
        public_key: str = settings.jwt.public_key_path.read_text()
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[settings.jwt.ALGORITHM])
    return decoded


def encode_jwt(
        payload: dict,
        private_key: str = settings.jwt.private_key_path.read_text(),
) -> str:
    encoded = jwt.encode(payload, private_key, algorithm=settings.jwt.ALGORITHM)
    return encoded


def create_access_token(
        payload: dict,
        access_token_expire_time: timedelta = timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = {
        "sub": payload,
        "exp": datetime.now(UTC) + access_token_expire_time
    }
    return encode_jwt(to_encode)


def create_refresh_token(
        payload: dict,
        refresh_token_expire_time: timedelta = timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS)
) -> str:
    to_encode = {
        "sub": payload,
        "exp": datetime.now(UTC) + refresh_token_expire_time
    }
    return encode_jwt(to_encode)


def create_token_pair(
        access_token_payload: dict,
        refresh_token_payload: dict,
) -> TokenPair:
    return TokenPair(
        access_token=create_access_token(access_token_payload),
        refresh_token=create_refresh_token(refresh_token_payload)
    )

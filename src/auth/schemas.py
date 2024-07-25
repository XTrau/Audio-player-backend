from pydantic import BaseModel, EmailStr


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"


class SUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    hashed_password: str | None = None


class SUser(BaseModel):
    username: str
    email: EmailStr
    disabled: bool = False
    is_verified: bool = False


class SUserInDB(SUser):
    id: int
    hashed_password: str

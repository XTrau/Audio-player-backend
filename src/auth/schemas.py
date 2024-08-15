from pydantic import BaseModel, EmailStr


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"


class SUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class SUser(BaseModel):
    username: str
    email: EmailStr
    disabled: bool = False
    is_verified: bool = False
    is_superuser: bool = False


class SUserInDB(SUser):
    id: int
    hashed_password: str

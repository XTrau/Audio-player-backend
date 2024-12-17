from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class SUserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, max_length=64)

    @classmethod
    @field_validator("username", mode="before")
    def username_alphanumeric(cls, value: str):
        if not value.isalnum():
            raise ValueError(
                "Username пользователя может содержать только символы английского алфавита и цифры"
            )
        if not 5 <= len(value) <= 255:
            raise ValueError(
                "Минимальная длина поля username 5 символов, максимальная - 255 символа"
            )
        return value


class SUserLogin(BaseModel):
    login: str
    password: str


class SUser(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool


class SUserInDB(SUser):
    id: int
    hashed_password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

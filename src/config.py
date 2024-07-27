from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DB_Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")


class JWT_Settings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private_key.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public_key.pem"
    algorithm: str = "RS256"

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    access_token_expire_seconds: int = access_token_expire_minutes * 60
    refresh_token_expire_seconds: int = refresh_token_expire_days * 24 * 60 * 60

    access_token_type: str = "access"
    refresh_token_type: str = "refresh"


class Settings(BaseSettings):
    db: DB_Settings = DB_Settings()
    jwt: JWT_Settings = JWT_Settings()


settings = Settings()

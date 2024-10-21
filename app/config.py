import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    FR_DB_USER: str
    DB_PASS: str
    SECRET_KEY: str
    ALGORITHM: str
    GOOGLE_MAPS_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    result =  (f"postgresql+asyncpg://{settings.FR_DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(result)
    return result


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

#print(get_db_url())

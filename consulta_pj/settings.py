from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    app_title: str = "JPData Integrator"
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""

    @property
    def db_uri(self) -> str:
        uri = f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        return uri


@lru_cache()
def get_settings() -> Settings:
    return Settings()

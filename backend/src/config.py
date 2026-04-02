from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environments(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "dev"
    TESTING = "test"
    PRODUCTION = "prod"

class Settings (BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "family_budget_local"
    
    ENVIRONMENT: Environments = Environments.LOCAL

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        extra="ignore",
    )

settings = Settings()

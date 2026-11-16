from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    APP_NAME: str = "Finance Trace"
    ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    FIELD_ENCRYPTION_KEY: str = ""
    JWT_SECRET: str = "dev-only-secret-change-me"
    DATABASE_URL: str = "postgresql+psycopg://fintrace:fintrace_dev_pw@db:5432/fintrace"
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_MB: int = 100

@lru_cache
def get_settings() -> Settings:
    return Settings()

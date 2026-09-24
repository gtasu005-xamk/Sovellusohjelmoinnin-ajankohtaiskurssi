from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    POSTGRES_USER: str = "username"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "appdb"
    DATABASE_URL: str = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173"
    SQLADMIN_USERNAME: str = "admin"
    SQLADMIN_PASSWORD: str = "admin"
    SQLADMIN_SECRET_KEY: str = "vaihdaminut"
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
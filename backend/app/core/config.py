from pydantic_settings import BaseSettings

class Settings(BaseSettings):
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


settings = Settings()
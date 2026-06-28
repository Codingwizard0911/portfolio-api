from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/portfolio"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = [
        "https://portfolio-self-two-97.vercel.app",
        "https://umapathi.dev",
    ]
    ALLOWED_HOSTS: List[str] = [
        "umapathi-portfolio-api.onrender.com",
        "localhost",
        "127.0.0.1",
    ]
    CONTACT_EMAIL: str = "umapathiu0911@gmail.com"
    SECRET_KEY: str = "change-me-in-production"

    class Config:
        env_file = ".env"


settings = Settings()

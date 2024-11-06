from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal, Optional
import os


class BaseAppSettings(BaseSettings):
    """Base application settings."""
    APP_NAME: str = "Candidate Management System"
    API_V1_PREFIX: str = "/api/v1"
    APP_ENV: Literal["local", "development", "production"] = "local"

    # MongoDB
    MONGODB_URL: Optional[str] = None
    MONGODB_DB_NAME: Optional[str] = None

    # JWT
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis
    REDIS_URL: Optional[str] = None

    # Sentry
    SENTRY_DSN: Optional[str] = None


class LocalSettings(BaseAppSettings):
    """Local environment settings."""
    APP_ENV: Literal["local"] = "local"

    class Config:
        env_file = ".env"


class DevelopmentSettings(BaseAppSettings):
    """Development environment settings."""
    APP_ENV: Literal["development"] = "development"
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    REDIS_URL: str = os.getenv("REDIS_URL")


class ProductionSettings(BaseAppSettings):
    """Production environment settings."""
    APP_ENV: Literal["production"] = "production"
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    REDIS_URL: str = os.getenv("REDIS_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)


@lru_cache()
def get_settings() -> BaseAppSettings:
    """
    Factory function to get the appropriate settings based on the environment.
    Prioritizes the APP_ENV environment variable over the default value.
    """
    app_env = os.getenv("APP_ENV", "local").lower()
    if app_env == "local":
        return LocalSettings()
    elif app_env == "development":
        return DevelopmentSettings()
    elif app_env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Invalid APP_ENV: {app_env}")
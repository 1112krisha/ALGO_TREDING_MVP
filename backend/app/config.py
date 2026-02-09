"""
Application configuration via environment variables.

Supports .env files for local development.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    # App
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production-use-env-var"
    
    # Database: SQLite by default, PostgreSQL for production
    DATABASE_URL: str = "sqlite+aiosqlite:///./algo_trading.db"
    
    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Trading engine
    PRICE_POLL_INTERVAL_SECONDS: int = 5
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

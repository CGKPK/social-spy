"""
Backend configuration using pydantic-settings.
Loads from .env file while maintaining backward compatibility with config.py.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    grok_api_key: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    meta_access_token: Optional[str] = None
    linkedin_access_token: Optional[str] = None

    # Settings
    check_interval: int = 30
    max_posts_per_platform: int = 500

    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    # Data files
    data_file: str = "social_data.json"
    manual_entries_file: str = "manual_entries.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()

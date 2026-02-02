"""
Pydantic models for configuration.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class YouTubeChannel(BaseModel):
    """YouTube channel configuration."""
    name: str
    channel_id: str


class ConfigResponse(BaseModel):
    """Configuration response model."""
    keywords: List[str]
    youtube_channels: List[YouTubeChannel]
    twitter_accounts: List[str]
    grok_x_accounts: List[str]
    meta_pages: List[Dict[str, str]]
    linkedin_companies: List[Dict[str, str]]
    check_interval: int
    max_posts_per_platform: int
    api_configured: Dict[str, bool]


class KeywordsUpdate(BaseModel):
    """Update keywords request."""
    keywords: List[str] = Field(..., min_length=1)


class YouTubeChannelsUpdate(BaseModel):
    """Update YouTube channels request."""
    channels: List[YouTubeChannel]


class TwitterAccountsUpdate(BaseModel):
    """Update Twitter accounts request."""
    accounts: List[str]


class APIKeyUpdate(BaseModel):
    """Update API key request."""
    api_key: str = Field(..., min_length=1)

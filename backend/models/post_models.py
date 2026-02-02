"""
Pydantic models for social media posts.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    """Base post model matching the data structure in social_data.json."""
    platform: str
    type: str
    id: str
    text: Optional[str] = None
    url: Optional[str] = None
    author: Optional[str] = None
    published: Optional[str] = None
    fetched_at: Optional[str] = None
    likes: Optional[int] = 0
    comments: Optional[int] = 0
    shares: Optional[int] = 0
    retweets: Optional[int] = 0
    views: Optional[int] = 0
    channel_name: Optional[str] = None
    channel_id: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[str] = None
    tags: Optional[List[str]] = []


class PostResponse(BaseModel):
    """Response model for paginated posts."""
    posts: List[PostBase]
    total: int
    limit: int
    offset: int


class PostStats(BaseModel):
    """Statistics about posts."""
    total_posts: int
    by_platform: Dict[str, int]
    by_type: Dict[str, int]
    total_likes: int
    total_comments: int
    total_shares: int
    last_updated: Optional[str] = None


class PostFilter(BaseModel):
    """Filters for querying posts."""
    platform: Optional[str] = None
    type: Optional[str] = None
    author: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)

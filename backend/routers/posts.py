"""
Posts API routes.
"""
from fastapi import APIRouter, Query
from typing import Optional

from ..models.post_models import PostResponse, PostStats
from ..services.data_service import DataService

router = APIRouter(prefix="/posts", tags=["posts"])
data_service = DataService()


@router.get("/", response_model=PostResponse)
async def get_posts(
    platform: Optional[str] = None,
    type: Optional[str] = None,
    author: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """
    Get posts with optional filtering and pagination.

    - **platform**: Filter by platform (youtube, twitter, meta, linkedin)
    - **type**: Filter by post type (video, tweet, post, etc.)
    - **author**: Filter by author name (partial match)
    - **date_from**: Filter posts from this date (ISO format)
    - **date_to**: Filter posts until this date (ISO format)
    - **limit**: Number of posts to return (1-500)
    - **offset**: Number of posts to skip
    """
    result = data_service.filter_posts(
        platform=platform,
        post_type=type,
        author=author,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return PostResponse(**result)


@router.get("/stats", response_model=PostStats)
async def get_stats():
    """Get aggregated statistics about posts."""
    stats = data_service.get_stats()
    return PostStats(**stats)


@router.get("/recent", response_model=PostResponse)
async def get_recent_posts(
    days: int = Query(default=7, ge=1, le=365),
    limit: int = Query(default=50, ge=1, le=500),
):
    """Get recent posts from the last N days."""
    posts = data_service.get_recent_posts(days=days, limit=limit)
    return PostResponse(
        posts=posts,
        total=len(posts),
        limit=limit,
        offset=0,
    )

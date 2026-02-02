"""
Configuration API routes.
"""
import sys
import os
from fastapi import APIRouter, HTTPException

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config
from ..models.config_models import (
    ConfigResponse,
    KeywordsUpdate,
    YouTubeChannelsUpdate,
    TwitterAccountsUpdate,
    YouTubeChannel,
)

router = APIRouter(prefix="/config", tags=["config"])


def _check_api_configured() -> dict:
    """Check which APIs are configured."""
    return {
        "youtube": True,  # Always available via RSS
        "twitter": bool(config.TWITTER_API.get("bearer_token")),
        "grok": bool(config.GROK_API.get("api_key")),
        "meta": bool(config.META_API.get("access_token")),
        "linkedin": bool(config.LINKEDIN_API.get("access_token")),
    }


@router.get("/", response_model=ConfigResponse)
async def get_config():
    """Get current configuration."""
    return ConfigResponse(
        keywords=config.KEYWORDS,
        youtube_channels=[
            YouTubeChannel(**ch) for ch in config.YOUTUBE_CHANNELS
        ],
        twitter_accounts=config.TWITTER_ACCOUNTS,
        grok_x_accounts=getattr(config, "GROK_X_ACCOUNTS", []),
        meta_pages=config.META_PAGES,
        linkedin_companies=config.LINKEDIN_COMPANIES,
        check_interval=config.CHECK_INTERVAL,
        max_posts_per_platform=config.MAX_POSTS_PER_PLATFORM,
        api_configured=_check_api_configured(),
    )


@router.put("/keywords")
async def update_keywords(request: KeywordsUpdate):
    """Update keywords list."""
    try:
        # Update in-memory config
        config.KEYWORDS = request.keywords

        # Write to config.py file
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config.py"
        )
        _update_config_file(config_path, "KEYWORDS", request.keywords)

        return {"message": "Keywords updated", "keywords": request.keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update keywords: {str(e)}")


@router.put("/channels/youtube")
async def update_youtube_channels(request: YouTubeChannelsUpdate):
    """Update YouTube channels list."""
    try:
        channels_list = [ch.dict() for ch in request.channels]
        config.YOUTUBE_CHANNELS = channels_list

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config.py"
        )
        _update_config_file(config_path, "YOUTUBE_CHANNELS", channels_list)

        return {"message": "YouTube channels updated", "channels": channels_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update channels: {str(e)}")


@router.put("/accounts/twitter")
async def update_twitter_accounts(request: TwitterAccountsUpdate):
    """Update Twitter accounts list."""
    try:
        config.TWITTER_ACCOUNTS = request.accounts

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config.py"
        )
        _update_config_file(config_path, "TWITTER_ACCOUNTS", request.accounts)

        return {"message": "Twitter accounts updated", "accounts": request.accounts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update accounts: {str(e)}")


def _update_config_file(config_path: str, key: str, value):
    """
    Update a value in config.py file.
    Note: This is a simple implementation. For production, consider using a proper config management system.
    """
    import re

    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the assignment and replace it
    pattern = rf"{key}\s*=\s*\[.*?\]"
    replacement = f"{key} = {repr(value)}"

    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # If not found, append at the end
        content += f"\n{replacement}\n"

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)

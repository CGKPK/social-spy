"""
YouTube Monitor
================
Uses RSS feeds to monitor YouTube channels without requiring API keys.
"""

import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import re


def get_channel_feed_url(channel_id: str) -> str:
    """Convert a channel ID to its RSS feed URL."""
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def get_user_feed_url(username: str) -> str:
    """Convert a username to its RSS feed URL."""
    return f"https://www.youtube.com/feeds/videos.xml?user={username}"


def parse_feed(feed_url: str, channel_name: str = "Unknown") -> List[Dict]:
    """
    Parse a YouTube RSS feed and return video entries.

    Args:
        feed_url: The RSS feed URL
        channel_name: Display name for the channel

    Returns:
        List of video dictionaries
    """
    videos = []

    try:
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            print(f"⚠️  Warning: Feed parsing issue for {channel_name}")

        for entry in feed.entries:
            video = {
                "platform": "youtube",
                "type": "video",
                "id": entry.get("yt_videoid", entry.get("id", "")),
                "title": entry.get("title", ""),
                "description": entry.get("summary", "")[:500],  # Truncate long descriptions
                "url": entry.get("link", ""),
                "author": entry.get("author", channel_name),
                "channel_name": channel_name,
                "published": entry.get("published", ""),
                "thumbnail": get_thumbnail(entry),
                "views": get_view_count(entry),
                "fetched_at": datetime.now().isoformat(),
            }
            videos.append(video)

    except Exception as e:
        print(f"❌ Error fetching YouTube feed for {channel_name}: {e}")

    return videos


def get_thumbnail(entry: Dict) -> str:
    """Extract thumbnail URL from feed entry."""
    # Try media:thumbnail
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url", "")

    # Try to construct from video ID
    video_id = entry.get("yt_videoid", "")
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"

    return ""


def get_view_count(entry: Dict) -> Optional[int]:
    """Extract view count if available."""
    if hasattr(entry, "media_statistics"):
        views = entry.media_statistics.get("views", 0)
        try:
            return int(views)
        except (ValueError, TypeError):
            pass
    return None


def fetch_all_channels(channels: List[Dict]) -> List[Dict]:
    """
    Fetch videos from multiple YouTube channels.

    Args:
        channels: List of channel dicts with 'name' and 'channel_id'

    Returns:
        Combined list of all videos
    """
    all_videos = []

    for channel in channels:
        name = channel.get("name", "Unknown")
        channel_id = channel.get("channel_id", "")

        if not channel_id:
            print(f"⚠️  Skipping {name}: No channel ID provided")
            continue

        print(f"📺 Fetching YouTube: {name}...")
        feed_url = get_channel_feed_url(channel_id)
        videos = parse_feed(feed_url, name)
        all_videos.extend(videos)
        print(f"   Found {len(videos)} videos")

    return all_videos


def search_videos_for_keywords(videos: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Filter videos that contain any of the specified keywords.

    Args:
        videos: List of video dictionaries
        keywords: List of keywords to search for

    Returns:
        Filtered list of matching videos
    """
    if not keywords:
        return videos

    matching = []
    patterns = [re.compile(re.escape(kw), re.IGNORECASE) for kw in keywords]

    for video in videos:
        text = f"{video.get('title', '')} {video.get('description', '')}"
        for pattern in patterns:
            if pattern.search(text):
                video["matched_keyword"] = pattern.pattern
                matching.append(video)
                break

    return matching


if __name__ == "__main__":
    # Test with a public channel
    test_channels = [
        {"name": "TED", "channel_id": "UCAuUUnT6oDeKwE6v1US8Lg"},
    ]

    videos = fetch_all_channels(test_channels)
    print(f"\nFetched {len(videos)} total videos")

    for video in videos[:3]:
        print(f"  - {video['title'][:50]}...")

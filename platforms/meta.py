"""
Meta (Facebook/Instagram) Monitor
===================================
Uses the Meta Graph API to monitor pages you manage.
Requires API credentials from https://developers.facebook.com/
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional


class MetaMonitor:
    """Monitor Facebook and Instagram pages via Graph API."""

    GRAPH_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, access_token: str):
        """
        Initialize the Meta monitor.

        Args:
            access_token: Page Access Token with required permissions
        """
        self.access_token = access_token

    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        return bool(self.access_token)

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to the Graph API."""
        if params is None:
            params = {}
        params["access_token"] = self.access_token

        try:
            response = requests.get(f"{self.GRAPH_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Meta API error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Meta error: {e}")
            return None

    def get_page_posts(self, page_id: str, limit: int = 25) -> List[Dict]:
        """
        Get recent posts from a Facebook page.

        Args:
            page_id: The Facebook Page ID
            limit: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        if not self.is_configured():
            print("⚠️  Meta API not configured - skipping")
            return []

        posts = []
        params = {
            "fields": "id,message,created_time,permalink_url,shares,likes.summary(true),comments.summary(true),attachments",
            "limit": limit,
        }

        data = self._make_request(f"{page_id}/posts", params)

        if data and "data" in data:
            for post in data["data"]:
                attachments = post.get("attachments", {}).get("data", [{}])
                attachment = attachments[0] if attachments else {}

                posts.append({
                    "platform": "facebook",
                    "type": "post",
                    "id": post.get("id", ""),
                    "text": post.get("message", ""),
                    "url": post.get("permalink_url", ""),
                    "published": post.get("created_time", ""),
                    "likes": post.get("likes", {}).get("summary", {}).get("total_count", 0),
                    "comments": post.get("comments", {}).get("summary", {}).get("total_count", 0),
                    "shares": post.get("shares", {}).get("count", 0),
                    "media_type": attachment.get("type", ""),
                    "media_url": attachment.get("url", ""),
                    "fetched_at": datetime.now().isoformat(),
                })

        return posts

    def get_instagram_media(self, ig_user_id: str, limit: int = 25) -> List[Dict]:
        """
        Get recent media from an Instagram Business account.

        Args:
            ig_user_id: The Instagram Business Account ID
            limit: Maximum number of posts to fetch

        Returns:
            List of media dictionaries
        """
        if not self.is_configured():
            print("⚠️  Meta API not configured - skipping")
            return []

        posts = []
        params = {
            "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,thumbnail_url",
            "limit": limit,
        }

        data = self._make_request(f"{ig_user_id}/media", params)

        if data and "data" in data:
            for media in data["data"]:
                posts.append({
                    "platform": "instagram",
                    "type": media.get("media_type", "IMAGE").lower(),
                    "id": media.get("id", ""),
                    "text": media.get("caption", ""),
                    "url": media.get("permalink", ""),
                    "published": media.get("timestamp", ""),
                    "likes": media.get("like_count", 0),
                    "comments": media.get("comments_count", 0),
                    "media_url": media.get("media_url", media.get("thumbnail_url", "")),
                    "fetched_at": datetime.now().isoformat(),
                })

        return posts

    def search_page_mentions(self, page_id: str, limit: int = 25) -> List[Dict]:
        """
        Get posts that mention a Facebook page (requires Page Public Content Access).

        Args:
            page_id: The Facebook Page ID
            limit: Maximum number of mentions to fetch

        Returns:
            List of mention dictionaries
        """
        if not self.is_configured():
            return []

        # Note: This requires elevated permissions
        params = {
            "fields": "id,message,created_time,from,permalink_url",
            "limit": limit,
        }

        data = self._make_request(f"{page_id}/tagged", params)
        mentions = []

        if data and "data" in data:
            for post in data["data"]:
                mentions.append({
                    "platform": "facebook",
                    "type": "mention",
                    "id": post.get("id", ""),
                    "text": post.get("message", ""),
                    "url": post.get("permalink_url", ""),
                    "author": post.get("from", {}).get("name", "Unknown"),
                    "published": post.get("created_time", ""),
                    "fetched_at": datetime.now().isoformat(),
                })

        return mentions

    def fetch_all_pages(self, pages: List[Dict]) -> List[Dict]:
        """
        Fetch posts from multiple Facebook/Instagram pages.

        Args:
            pages: List of page dicts with 'name', 'page_id', and optional 'instagram_id'

        Returns:
            Combined list of posts
        """
        all_posts = []

        for page in pages:
            name = page.get("name", "Unknown")
            page_id = page.get("page_id", "")
            instagram_id = page.get("instagram_id", "")

            if page_id:
                print(f"📘 Fetching Facebook: {name}...")
                posts = self.get_page_posts(page_id)
                all_posts.extend(posts)
                print(f"   Found {len(posts)} Facebook posts")

            if instagram_id:
                print(f"📸 Fetching Instagram: {name}...")
                media = self.get_instagram_media(instagram_id)
                all_posts.extend(media)
                print(f"   Found {len(media)} Instagram posts")

        return all_posts


def create_monitor(config: Dict) -> MetaMonitor:
    """Create a Meta monitor from config."""
    return MetaMonitor(config.get("access_token", ""))


if __name__ == "__main__":
    # Test - requires valid access token
    monitor = MetaMonitor("")
    if monitor.is_configured():
        print("Meta API configured - ready to fetch")
    else:
        print("Meta API not configured - add access_token to test")

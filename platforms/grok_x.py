"""
Grok X Monitor
==============
Uses xAI's Grok API with x_search tool to monitor X/Twitter posts.
Requires API key from https://console.x.ai/

Grok has direct real-time access to X data, making it ideal for
social media monitoring without needing separate Twitter API access.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from xai_sdk import Client
    from xai_sdk.chat import user, system
    from xai_sdk.tools import x_search
    XAI_SDK_AVAILABLE = True
except ImportError:
    XAI_SDK_AVAILABLE = False


class GrokXMonitor:
    """Monitor X/Twitter using Grok's x_search capability."""

    def __init__(self, api_key: str):
        """
        Initialize the Grok X monitor.

        Args:
            api_key: xAI API key from console.x.ai
        """
        self.api_key = api_key
        self.client = None

        if XAI_SDK_AVAILABLE and api_key:
            self.client = Client(api_key=api_key)

    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        if not XAI_SDK_AVAILABLE:
            return False
        return bool(self.api_key)

    def _parse_posts_from_response(self, response_text: str) -> List[Dict]:
        """
        Parse structured post data from Grok's response.

        Args:
            response_text: The text response from Grok

        Returns:
            List of parsed post dictionaries
        """
        posts = []

        # Try to extract JSON array from response
        json_match = re.search(r'\[\s*\{.*?\}\s*\]', response_text, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                for item in parsed:
                    post = self._normalize_post(item)
                    if post:
                        posts.append(post)
                return posts
            except json.JSONDecodeError:
                pass

        # Fallback: parse individual JSON objects
        json_objects = re.findall(r'\{[^{}]*"(?:text|content|tweet)"[^{}]*\}', response_text, re.DOTALL)
        for obj_str in json_objects:
            try:
                item = json.loads(obj_str)
                post = self._normalize_post(item)
                if post:
                    posts.append(post)
            except json.JSONDecodeError:
                continue

        return posts

    def _normalize_post(self, item: Dict) -> Optional[Dict]:
        """
        Normalize a parsed post to the standard schema.

        Args:
            item: Raw parsed post data

        Returns:
            Normalized post dictionary or None if invalid
        """
        # Extract text (various possible field names)
        text = (
            item.get("text") or
            item.get("content") or
            item.get("tweet") or
            item.get("body") or
            ""
        )

        if not text:
            return None

        # Extract URL
        url = item.get("url") or item.get("link") or ""

        # Try to extract post ID from URL
        post_id = item.get("id") or ""
        if not post_id and url:
            id_match = re.search(r'/status/(\d+)', url)
            if id_match:
                post_id = id_match.group(1)
        if not post_id:
            # Generate a hash-based ID as fallback
            post_id = str(hash(text))[:12]

        # Extract author info
        author = (
            item.get("author") or
            item.get("username") or
            item.get("user") or
            item.get("name") or
            "Unknown"
        )
        author_username = item.get("username") or item.get("handle") or ""
        if author_username and not author_username.startswith("@"):
            author_username = f"@{author_username}"

        # Extract metrics (Grok may not always provide these)
        likes = int(item.get("likes", 0) or item.get("like_count", 0) or 0)
        retweets = int(item.get("retweets", 0) or item.get("retweet_count", 0) or 0)
        replies = int(item.get("replies", 0) or item.get("reply_count", 0) or 0)
        views = int(item.get("views", 0) or item.get("view_count", 0) or 0)

        # Extract timestamp
        published = item.get("published") or item.get("date") or item.get("created_at") or ""

        return {
            "platform": "twitter",
            "type": "tweet",
            "id": str(post_id),
            "text": text.strip(),
            "url": url,
            "author": author,
            "author_username": author_username,
            "published": published,
            "likes": likes,
            "retweets": retweets,
            "replies": replies,
            "views": views,
            "fetched_at": datetime.now().isoformat(),
            "source": "grok",
        }

    def search_keywords(
        self,
        keywords: List[str],
        max_results: int = 20,
        days_back: int = 7
    ) -> List[Dict]:
        """
        Search X for posts matching keywords using Grok.

        Args:
            keywords: List of keywords to search
            max_results: Maximum posts to return per keyword
            days_back: How many days back to search

        Returns:
            List of post dictionaries
        """
        if not self.is_configured():
            print("⚠️  Grok API not configured - skipping X search")
            return []

        all_posts = []
        seen_ids = set()

        # Calculate date range (must be datetime objects, not strings)
        from_date = datetime.now() - timedelta(days=days_back)
        to_date = datetime.now()

        for keyword in keywords:
            print(f"🤖 Grok searching X for: {keyword}...")

            try:
                posts = self._search_single_keyword(keyword, max_results, from_date, to_date)

                for post in posts:
                    if post["id"] not in seen_ids:
                        post["matched_keyword"] = keyword
                        all_posts.append(post)
                        seen_ids.add(post["id"])

                print(f"   Found {len(posts)} posts")

            except Exception as e:
                print(f"   ❌ Error searching for '{keyword}': {e}")

        return all_posts

    def _search_single_keyword(
        self,
        keyword: str,
        max_results: int,
        from_date: datetime,
        to_date: datetime
    ) -> List[Dict]:
        """
        Search for a single keyword on X.

        Args:
            keyword: Search term
            max_results: Maximum results to return
            from_date: Start datetime
            to_date: End datetime

        Returns:
            List of post dictionaries
        """
        # Create a chat with x_search tool enabled
        chat = self.client.chat.create(
            model="grok-4-fast",
            tools=[
                x_search(from_date=from_date, to_date=to_date),
            ],
        )

        # Craft prompt for structured output
        prompt = f"""Search X (Twitter) for posts about "{keyword}" from the last week.

Return the results as a JSON array with this exact format:
[
  {{
    "text": "the tweet text",
    "url": "https://x.com/username/status/123",
    "author": "Display Name",
    "username": "handle",
    "published": "2026-01-28T12:00:00Z",
    "likes": 100,
    "retweets": 50,
    "replies": 25
  }}
]

Find up to {max_results} relevant posts. Only return the JSON array, no other text."""

        chat.append(user(prompt))

        # Get response (non-streaming for simplicity)
        response = chat.sample()
        response_text = response.content if hasattr(response, 'content') else str(response)

        return self._parse_posts_from_response(response_text)

    def search_accounts(
        self,
        accounts: List[str],
        max_results: int = 10
    ) -> List[Dict]:
        """
        Get recent posts from specific X accounts.

        Args:
            accounts: List of usernames to monitor (with or without @)
            max_results: Maximum posts per account

        Returns:
            List of post dictionaries
        """
        if not self.is_configured():
            print("⚠️  Grok API not configured - skipping X account fetch")
            return []

        all_posts = []
        seen_ids = set()

        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()

        for account in accounts:
            # Clean up account name
            account = account.lstrip("@")
            print(f"🤖 Grok fetching X account: @{account}...")

            try:
                chat = self.client.chat.create(
                    model="grok-4-fast",
                    tools=[
                        x_search(from_date=from_date, to_date=to_date),
                    ],
                )

                prompt = f"""Get the {max_results} most recent posts from X user @{account}.

Return the results as a JSON array with this exact format:
[
  {{
    "text": "the tweet text",
    "url": "https://x.com/{account}/status/123",
    "author": "Display Name",
    "username": "{account}",
    "published": "2026-01-28T12:00:00Z",
    "likes": 100,
    "retweets": 50,
    "replies": 25
  }}
]

Only return the JSON array, no other text."""

                chat.append(user(prompt))
                response = chat.sample()
                response_text = response.content if hasattr(response, 'content') else str(response)

                posts = self._parse_posts_from_response(response_text)

                for post in posts:
                    if post["id"] not in seen_ids:
                        all_posts.append(post)
                        seen_ids.add(post["id"])

                print(f"   Found {len(posts)} posts")

            except Exception as e:
                print(f"   ❌ Error fetching @{account}: {e}")

        return all_posts


def create_monitor(config: Dict) -> GrokXMonitor:
    """Create a Grok X monitor from config."""
    api_key = config.get("api_key", "") or os.getenv("XAI_API_KEY", "")
    return GrokXMonitor(api_key)


if __name__ == "__main__":
    # Test - requires valid API key
    api_key = os.getenv("XAI_API_KEY", "")
    monitor = GrokXMonitor(api_key)

    if monitor.is_configured():
        print("Testing Grok X search...")
        posts = monitor.search_keywords(["python programming"], max_results=5)
        print(f"Found {len(posts)} posts")
        for post in posts[:3]:
            print(f"  - @{post.get('author_username', 'unknown')}: {post['text'][:80]}...")
    else:
        print("Grok API not configured - set XAI_API_KEY environment variable")
        print("Or add api_key to GROK_API in config.py")

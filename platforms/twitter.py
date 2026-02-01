"""
X/Twitter Monitor
==================
Uses the X API v2 to monitor tweets and mentions.
Requires API credentials from https://developer.twitter.com/
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re


class TwitterMonitor:
    """Monitor X/Twitter for posts and mentions."""

    BASE_URL = "https://api.twitter.com/2"

    def __init__(self, bearer_token: str):
        """
        Initialize the Twitter monitor.

        Args:
            bearer_token: X API Bearer Token
        """
        self.bearer_token = bearer_token
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        return bool(self.bearer_token)

    def search_recent(
        self, query: str, max_results: int = 100, since_hours: int = 24
    ) -> List[Dict]:
        """
        Search for recent tweets matching a query.

        Args:
            query: Search query (supports X search operators)
            max_results: Maximum number of results (10-100)
            since_hours: How far back to search (max 7 days for basic API)

        Returns:
            List of tweet dictionaries
        """
        if not self.is_configured():
            print("⚠️  Twitter API not configured - skipping")
            return []

        tweets = []
        endpoint = f"{self.BASE_URL}/tweets/search/recent"

        # Calculate start time
        start_time = (datetime.utcnow() - timedelta(hours=since_hours)).isoformat() + "Z"

        params = {
            "query": query,
            "max_results": min(max_results, 100),
            "start_time": start_time,
            "tweet.fields": "created_at,public_metrics,author_id,conversation_id",
            "expansions": "author_id",
            "user.fields": "name,username,profile_image_url",
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Build user lookup
            users = {}
            if "includes" in data and "users" in data["includes"]:
                for user in data["includes"]["users"]:
                    users[user["id"]] = user

            # Process tweets
            for tweet in data.get("data", []):
                author = users.get(tweet["author_id"], {})
                metrics = tweet.get("public_metrics", {})

                tweets.append({
                    "platform": "twitter",
                    "type": "tweet",
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "url": f"https://twitter.com/{author.get('username', 'i')}/status/{tweet['id']}",
                    "author": author.get("name", "Unknown"),
                    "author_username": author.get("username", ""),
                    "author_avatar": author.get("profile_image_url", ""),
                    "published": tweet.get("created_at", ""),
                    "likes": metrics.get("like_count", 0),
                    "retweets": metrics.get("retweet_count", 0),
                    "replies": metrics.get("reply_count", 0),
                    "query": query,
                    "fetched_at": datetime.now().isoformat(),
                })

        except requests.exceptions.HTTPError as e:
            print(f"❌ Twitter API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"❌ Twitter error: {e}")

        return tweets

    def get_user_tweets(self, username: str, max_results: int = 10) -> List[Dict]:
        """
        Get recent tweets from a specific user.

        Args:
            username: Twitter username (without @)
            max_results: Maximum number of tweets to fetch

        Returns:
            List of tweet dictionaries
        """
        # Remove @ if present
        username = username.lstrip("@")
        query = f"from:{username}"
        return self.search_recent(query, max_results)

    def search_keywords(self, keywords: List[str], max_per_keyword: int = 50) -> List[Dict]:
        """
        Search for tweets containing any of the specified keywords.

        Args:
            keywords: List of keywords to search
            max_per_keyword: Max results per keyword

        Returns:
            Combined list of matching tweets
        """
        all_tweets = []
        seen_ids = set()

        for keyword in keywords:
            print(f"🐦 Searching Twitter for: {keyword}...")
            tweets = self.search_recent(keyword, max_per_keyword)

            for tweet in tweets:
                if tweet["id"] not in seen_ids:
                    tweet["matched_keyword"] = keyword
                    all_tweets.append(tweet)
                    seen_ids.add(tweet["id"])

            print(f"   Found {len(tweets)} tweets")

        return all_tweets

    def fetch_accounts(self, accounts: List[str]) -> List[Dict]:
        """
        Fetch recent tweets from multiple accounts.

        Args:
            accounts: List of usernames to monitor

        Returns:
            Combined list of tweets
        """
        all_tweets = []

        for account in accounts:
            print(f"🐦 Fetching Twitter: {account}...")
            tweets = self.get_user_tweets(account)
            all_tweets.extend(tweets)
            print(f"   Found {len(tweets)} tweets")

        return all_tweets


def create_monitor(config: Dict) -> TwitterMonitor:
    """Create a Twitter monitor from config."""
    return TwitterMonitor(config.get("bearer_token", ""))


if __name__ == "__main__":
    # Test - requires valid bearer token
    monitor = TwitterMonitor("")
    if monitor.is_configured():
        tweets = monitor.search_recent("python", max_results=10)
        print(f"Found {len(tweets)} tweets about Python")
    else:
        print("Twitter API not configured - add bearer_token to test")

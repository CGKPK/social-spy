"""
Data access service for JSON file operations.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class DataService:
    """Service for managing social_data.json."""

    def __init__(self, data_file: str = "social_data.json"):
        self.data_file = data_file

    def load_posts(self) -> Dict:
        """Load all data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        return {
            "posts": [],
            "last_updated": None,
            "stats": {},
        }

    def save_posts(self, data: Dict):
        """Save data to the JSON file."""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def filter_posts(
        self,
        platform: Optional[str] = None,
        post_type: Optional[str] = None,
        author: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict:
        """
        Filter and paginate posts.

        Returns:
            Dict with 'posts', 'total', 'limit', 'offset'
        """
        data = self.load_posts()
        posts = data.get("posts", [])

        # Apply filters
        filtered = posts

        if platform:
            filtered = [p for p in filtered if p.get("platform") == platform]

        if post_type:
            filtered = [p for p in filtered if p.get("type") == post_type]

        if author:
            filtered = [p for p in filtered if author.lower() in (p.get("author") or "").lower()]

        if date_from:
            filtered = [
                p for p in filtered
                if (p.get("published") or p.get("fetched_at", "")) >= date_from
            ]

        if date_to:
            filtered = [
                p for p in filtered
                if (p.get("published") or p.get("fetched_at", "")) <= date_to
            ]

        # Sort by published date (newest first)
        filtered.sort(
            key=lambda x: x.get("published") or x.get("fetched_at", ""),
            reverse=True
        )

        # Paginate
        total = len(filtered)
        paginated = filtered[offset:offset + limit]

        return {
            "posts": paginated,
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_stats(self) -> Dict:
        """Get statistics from the data."""
        data = self.load_posts()
        return data.get("stats", {})

    def get_recent_posts(self, days: int = 7, limit: int = 50) -> List[Dict]:
        """Get posts from the last N days."""
        from datetime import timedelta

        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        result = self.filter_posts(date_from=cutoff, limit=limit)
        return result["posts"]

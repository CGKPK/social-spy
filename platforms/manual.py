"""
Manual Entry Handler
======================
Allows manual addition of posts from any platform.
Useful for platforms without API access or for ad-hoc entries.
"""

from datetime import datetime
from typing import List, Dict, Optional
import json
import os


class ManualEntryManager:
    """Manage manually entered social media posts."""

    def __init__(self, data_file: str = "manual_entries.json"):
        """
        Initialize the manual entry manager.

        Args:
            data_file: Path to the JSON file storing manual entries
        """
        self.data_file = data_file
        self.entries = self._load_entries()

    def _load_entries(self) -> List[Dict]:
        """Load existing entries from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def _save_entries(self):
        """Save entries to file."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2, ensure_ascii=False)

    def add_entry(
        self,
        platform: str,
        text: str,
        url: str = "",
        author: str = "",
        post_type: str = "post",
        tags: List[str] = None,
        sentiment: str = "",
        notes: str = "",
    ) -> Dict:
        """
        Add a manual entry.

        Args:
            platform: Source platform (facebook, instagram, twitter, linkedin, youtube, other)
            text: The post content
            url: URL to the original post
            author: Author name/handle
            post_type: Type of content (post, comment, mention, review, etc.)
            tags: List of tags/categories
            sentiment: Sentiment (positive, negative, neutral)
            notes: Any additional notes

        Returns:
            The created entry
        """
        entry = {
            "platform": platform.lower(),
            "type": post_type,
            "id": f"manual_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "text": text,
            "url": url,
            "author": author,
            "published": datetime.now().isoformat(),
            "tags": tags or [],
            "sentiment": sentiment,
            "notes": notes,
            "source": "manual",
            "fetched_at": datetime.now().isoformat(),
        }

        self.entries.append(entry)
        self._save_entries()
        return entry

    def add_bulk(self, entries: List[Dict]) -> int:
        """
        Add multiple entries at once.

        Args:
            entries: List of entry dictionaries

        Returns:
            Number of entries added
        """
        count = 0
        for entry in entries:
            try:
                self.add_entry(
                    platform=entry.get("platform", "other"),
                    text=entry.get("text", ""),
                    url=entry.get("url", ""),
                    author=entry.get("author", ""),
                    post_type=entry.get("type", "post"),
                    tags=entry.get("tags", []),
                    sentiment=entry.get("sentiment", ""),
                    notes=entry.get("notes", ""),
                )
                count += 1
            except Exception as e:
                print(f"Error adding entry: {e}")

        return count

    def get_all_entries(self) -> List[Dict]:
        """Get all manual entries."""
        return self.entries

    def get_by_platform(self, platform: str) -> List[Dict]:
        """Get entries for a specific platform."""
        return [e for e in self.entries if e.get("platform", "").lower() == platform.lower()]

    def search(self, query: str) -> List[Dict]:
        """Search entries for a keyword."""
        query = query.lower()
        return [
            e for e in self.entries
            if query in e.get("text", "").lower()
            or query in e.get("author", "").lower()
            or query in str(e.get("tags", [])).lower()
        ]

    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry by ID."""
        initial_count = len(self.entries)
        self.entries = [e for e in self.entries if e.get("id") != entry_id]

        if len(self.entries) < initial_count:
            self._save_entries()
            return True
        return False

    def clear_all(self) -> int:
        """Clear all manual entries."""
        count = len(self.entries)
        self.entries = []
        self._save_entries()
        return count


def interactive_add():
    """Interactive CLI for adding manual entries."""
    manager = ManualEntryManager()

    print("\n📝 Manual Entry - Add Social Media Post")
    print("=" * 40)

    platforms = ["facebook", "instagram", "twitter", "linkedin", "youtube", "tiktok", "other"]
    print("Platforms:", ", ".join(platforms))
    platform = input("Platform: ").strip().lower() or "other"

    text = input("Post text/content: ").strip()
    url = input("URL (optional): ").strip()
    author = input("Author (optional): ").strip()

    sentiments = ["positive", "negative", "neutral", ""]
    print("Sentiments:", ", ".join(sentiments[:-1]))
    sentiment = input("Sentiment (optional): ").strip().lower()

    tags_input = input("Tags (comma-separated, optional): ").strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]

    notes = input("Notes (optional): ").strip()

    entry = manager.add_entry(
        platform=platform,
        text=text,
        url=url,
        author=author,
        sentiment=sentiment,
        tags=tags,
        notes=notes,
    )

    print(f"\n✅ Entry added with ID: {entry['id']}")
    return entry


if __name__ == "__main__":
    interactive_add()

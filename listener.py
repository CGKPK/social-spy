#!/usr/bin/env python3
"""
Social Media Listener
======================
Main entry point for the social media monitoring tool.

Usage:
    python listener.py              # Run once and generate dashboard
    python listener.py --watch      # Continuous monitoring mode
    python listener.py --add        # Add manual entry
    python listener.py --dashboard  # Only regenerate dashboard
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from platforms.youtube import fetch_all_channels as fetch_youtube, search_videos_for_keywords
from platforms.twitter import create_monitor as create_twitter_monitor
from platforms.meta import create_monitor as create_meta_monitor
from platforms.linkedin import create_monitor as create_linkedin_monitor
from platforms.grok_x import create_monitor as create_grok_monitor
from platforms.manual import ManualEntryManager
from dashboard import generate_dashboard
from analyze_trends import analyze_data, generate_report as generate_trend_report


class SocialMediaListener:
    """Main social media listening orchestrator."""

    def __init__(self):
        """Initialize the listener with configured monitors."""
        self.data_file = config.DATA_FILE
        self.data = self._load_data()

        # Initialize platform monitors
        self.twitter = create_twitter_monitor(config.TWITTER_API)
        self.meta = create_meta_monitor(config.META_API)
        self.linkedin = create_linkedin_monitor(config.LINKEDIN_API)
        self.grok = create_grok_monitor(getattr(config, 'GROK_API', {}))
        self.manual = ManualEntryManager()

    def _load_data(self) -> Dict:
        """Load existing data from file."""
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

    def _save_data(self):
        """Save data to file."""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _deduplicate(self, posts: List[Dict]) -> List[Dict]:
        """Remove duplicate posts based on ID and platform."""
        seen = set()
        unique = []

        # First, add existing posts to seen set
        for post in self.data.get("posts", []):
            key = (post.get("platform", ""), post.get("id", ""))
            seen.add(key)

        # Add new unique posts
        for post in posts:
            key = (post.get("platform", ""), post.get("id", ""))
            if key not in seen:
                seen.add(key)
                unique.append(post)

        return unique

    def _trim_old_posts(self):
        """Trim posts to stay within limits."""
        max_posts = config.MAX_POSTS_PER_PLATFORM

        # Group by platform
        by_platform = {}
        for post in self.data["posts"]:
            platform = post.get("platform", "other")
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(post)

        # Trim each platform and recombine
        trimmed = []
        for platform, posts in by_platform.items():
            # Sort by published date (newest first)
            posts.sort(
                key=lambda x: x.get("published", x.get("fetched_at", "")),
                reverse=True
            )
            trimmed.extend(posts[:max_posts])

        self.data["posts"] = trimmed

    def fetch_all(self) -> Dict[str, int]:
        """
        Fetch posts from all configured platforms.

        Returns:
            Dictionary with count of new posts per platform
        """
        results = {}

        # YouTube (RSS feeds - no API key needed)
        print("\n📺 Fetching YouTube...")
        youtube_posts = fetch_youtube(config.YOUTUBE_CHANNELS)
        if config.KEYWORDS:
            youtube_posts = search_videos_for_keywords(youtube_posts, config.KEYWORDS)
        new_youtube = self._deduplicate(youtube_posts)
        results["youtube"] = len(new_youtube)
        self.data["posts"].extend(new_youtube)

        # Twitter/X (via native API or Grok)
        twitter_posts = []

        # Option 1: Use Grok for X searching (preferred - uses x_search tool)
        if self.grok.is_configured():
            print("\n🤖 Fetching X via Grok...")

            # Fetch from monitored accounts
            grok_accounts = getattr(config, 'GROK_X_ACCOUNTS', [])
            if grok_accounts:
                twitter_posts.extend(self.grok.search_accounts(grok_accounts))

            # Search for keywords
            if config.KEYWORDS:
                twitter_posts.extend(self.grok.search_keywords(config.KEYWORDS))

        # Option 2: Fall back to native Twitter API if configured
        elif self.twitter.is_configured():
            print("\n🐦 Fetching Twitter/X...")

            # Fetch from monitored accounts
            if config.TWITTER_ACCOUNTS:
                twitter_posts.extend(self.twitter.fetch_accounts(config.TWITTER_ACCOUNTS))

            # Search for keywords
            if config.KEYWORDS:
                twitter_posts.extend(self.twitter.search_keywords(config.KEYWORDS))
        else:
            print("\n⚠️  Twitter/X: Not configured")
            print("   Option 1: Add api_key to GROK_API (recommended)")
            print("   Option 2: Add bearer_token to TWITTER_API")

        new_twitter = self._deduplicate(twitter_posts)
        results["twitter"] = len(new_twitter)
        self.data["posts"].extend(new_twitter)

        # Meta (Facebook/Instagram)
        if self.meta.is_configured():
            print("\n📘 Fetching Facebook/Instagram...")
            meta_posts = self.meta.fetch_all_pages(config.META_PAGES)
            new_meta = self._deduplicate(meta_posts)
            results["meta"] = len(new_meta)
            self.data["posts"].extend(new_meta)
        else:
            print("\n⚠️  Meta (Facebook/Instagram): Not configured (add access_token to config)")
            results["meta"] = 0

        # LinkedIn
        if self.linkedin.is_configured():
            print("\n💼 Fetching LinkedIn...")
            linkedin_posts = self.linkedin.fetch_all_companies(config.LINKEDIN_COMPANIES)
            new_linkedin = self._deduplicate(linkedin_posts)
            results["linkedin"] = len(new_linkedin)
            self.data["posts"].extend(new_linkedin)
        else:
            print("\n⚠️  LinkedIn: Not configured (add access_token to config)")
            results["linkedin"] = 0

        # Manual entries
        manual_entries = self.manual.get_all_entries()
        new_manual = self._deduplicate(manual_entries)
        results["manual"] = len(new_manual)
        self.data["posts"].extend(new_manual)

        # Trim and save
        self._trim_old_posts()
        self._update_stats()
        self._save_data()

        return results

    def _update_stats(self):
        """Calculate and update statistics."""
        posts = self.data["posts"]

        # Count by platform
        by_platform = {}
        for post in posts:
            platform = post.get("platform", "other")
            by_platform[platform] = by_platform.get(platform, 0) + 1

        # Count by type
        by_type = {}
        for post in posts:
            post_type = post.get("type", "post")
            by_type[post_type] = by_type.get(post_type, 0) + 1

        # Engagement totals
        total_likes = sum(post.get("likes", 0) for post in posts)
        total_comments = sum(post.get("comments", 0) for post in posts)
        total_shares = sum(
            post.get("shares", 0) + post.get("retweets", 0)
            for post in posts
        )

        self.data["stats"] = {
            "total_posts": len(posts),
            "by_platform": by_platform,
            "by_type": by_type,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "last_updated": datetime.now().isoformat(),
        }

    def generate_report(self) -> str:
        """Generate the HTML dashboard."""
        output_path = config.DASHBOARD_FILE
        generate_dashboard(self.data, output_path)
        return output_path

    def generate_trends(self) -> str:
        """Generate the trend analysis report."""
        output_path = "trend_report.md"
        analysis = analyze_data(self.data)
        report = generate_trend_report(analysis)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        return output_path

    def print_summary(self, results: Dict[str, int]):
        """Print a summary of the fetch results."""
        print("\n" + "=" * 50)
        print("📊 FETCH SUMMARY")
        print("=" * 50)

        total_new = sum(results.values())
        print(f"New posts found: {total_new}")

        for platform, count in results.items():
            icon = {
                "youtube": "📺",
                "twitter": "🐦",
                "meta": "📘",
                "linkedin": "💼",
                "manual": "📝",
            }.get(platform, "📌")
            print(f"  {icon} {platform.capitalize()}: {count}")

        print(f"\nTotal posts in database: {len(self.data['posts'])}")
        print(f"Last updated: {self.data.get('last_updated', 'Never')}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Social Media Listener")
    parser.add_argument("--watch", action="store_true", help="Continuous monitoring mode")
    parser.add_argument("--add", action="store_true", help="Add manual entry")
    parser.add_argument("--dashboard", action="store_true", help="Only regenerate dashboard")
    parser.add_argument("--interval", type=int, default=config.CHECK_INTERVAL,
                       help="Check interval in minutes (for --watch mode)")
    args = parser.parse_args()

    listener = SocialMediaListener()

    if args.add:
        # Interactive manual entry
        from platforms.manual import interactive_add
        interactive_add()
        print("\nRegenerating dashboard...")
        listener.data = listener._load_data()
        listener.data["posts"].extend(listener.manual.get_all_entries())
        listener._update_stats()
        listener._save_data()
        dashboard_path = listener.generate_report()
        print(f"✅ Dashboard updated: {dashboard_path}")
        trends_path = listener.generate_trends()
        print(f"📊 Trend report updated: {trends_path}")

    elif args.dashboard:
        # Just regenerate dashboard
        print("Regenerating dashboard...")
        dashboard_path = listener.generate_report()
        print(f"✅ Dashboard: {dashboard_path}")

    elif args.watch:
        # Continuous monitoring
        import time
        print(f"🔄 Starting continuous monitoring (every {args.interval} minutes)")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                results = listener.fetch_all()
                listener.print_summary(results)
                dashboard_path = listener.generate_report()
                print(f"✅ Dashboard updated: {dashboard_path}")
                trends_path = listener.generate_trends()
                print(f"📊 Trend report updated: {trends_path}")
                print(f"\n⏳ Next check in {args.interval} minutes...")
                time.sleep(args.interval * 60)
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped")

    else:
        # Single run
        print("🚀 Social Media Listener")
        print("=" * 50)
        results = listener.fetch_all()
        listener.print_summary(results)
        dashboard_path = listener.generate_report()
        print(f"\n✅ Dashboard generated: {dashboard_path}")
        trends_path = listener.generate_trends()
        print(f"📊 Trend report generated: {trends_path}")
        print("   Open these files to view results")


if __name__ == "__main__":
    main()

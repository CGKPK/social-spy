#!/usr/bin/env python3
"""
YouTube Channel ID Lookup Tool
===============================
Run this script to look up channel IDs from YouTube URLs/handles.

Usage:
    python lookup_channel_ids.py
"""

import re
import requests
from typing import Optional


def get_channel_id(url_or_handle: str) -> Optional[str]:
    """
    Look up the channel ID from a YouTube URL or handle.

    Args:
        url_or_handle: YouTube channel URL or @handle

    Returns:
        Channel ID (UC...) or None if not found
    """
    # Clean up input
    url_or_handle = url_or_handle.strip()

    # If it's already a channel ID
    if url_or_handle.startswith("UC") and len(url_or_handle) == 24:
        return url_or_handle

    # Build URL if needed
    if url_or_handle.startswith("@"):
        url = f"https://www.youtube.com/{url_or_handle}"
    elif not url_or_handle.startswith("http"):
        url = f"https://www.youtube.com/@{url_or_handle}"
    else:
        url = url_or_handle

    # If URL already contains channel ID
    match = re.search(r"/channel/(UC[a-zA-Z0-9_-]{22})", url)
    if match:
        return match.group(1)

    try:
        # Fetch the page and extract channel ID
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Look for channel ID in page source
        patterns = [
            r'"channelId":"(UC[a-zA-Z0-9_-]{22})"',
            r'"externalId":"(UC[a-zA-Z0-9_-]{22})"',
            r'/channel/(UC[a-zA-Z0-9_-]{22})',
        ]

        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)

    except Exception as e:
        print(f"  Error fetching {url}: {e}")

    return None


def main():
    """Look up channel IDs for the configured channels."""
    channels = [
        ("The Futures Desk", "https://www.youtube.com/@TheFuturesDesk"),
        ("Prop Firm Match", "https://www.youtube.com/@propfirmmatch"),
        ("My Funded Futures", "https://www.youtube.com/@MyFundedFuturesPropFirm"),
        ("Day Trading Jesus", "https://www.youtube.com/@daytradingjesus"),
        ("Kimmel Trading", "https://www.youtube.com/@KimmelTrading"),
        ("Jason Graystone", "https://www.youtube.com/@JasonGraystone"),
        ("Kelly Ann Trading", "https://www.youtube.com/@FuturesTradingwithKellyAnn"),
        ("Real Deal Futures", "https://www.youtube.com/@RealDealFutures"),
        ("Trade Pro", "https://www.youtube.com/channel/UCWoWTvvwhfuAqDuxYJHa03Q"),
        ("Mike Swartz", "https://www.youtube.com/@Mike_Swartz"),
    ]

    print("🔍 Looking up YouTube Channel IDs...\n")

    results = []
    for name, url in channels:
        print(f"  {name}...", end=" ", flush=True)
        channel_id = get_channel_id(url)
        if channel_id:
            print(f"✅ {channel_id}")
            results.append((name, channel_id))
        else:
            print("❌ Not found")
            results.append((name, None))

    print("\n" + "=" * 60)
    print("📋 Copy this to your config.py:\n")
    print("YOUTUBE_CHANNELS = [")
    for name, channel_id in results:
        if channel_id:
            print(f'    {{"name": "{name}", "channel_id": "{channel_id}"}},')
        else:
            print(f'    # {{"name": "{name}", "channel_id": "NOT_FOUND"}},')
    print("]")


if __name__ == "__main__":
    main()

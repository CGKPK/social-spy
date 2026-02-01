# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Social Media Listener - A Python tool that aggregates posts from multiple social platforms (YouTube, Twitter/X, Facebook/Instagram, LinkedIn) into an interactive HTML dashboard. YouTube monitoring uses RSS feeds (no API key required); other platforms require API credentials configured in `config.py`.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run once - fetch all platforms and generate dashboard
python listener.py

# Continuous monitoring (checks every 30 minutes by default)
python listener.py --watch
python listener.py --watch --interval 60  # custom interval in minutes

# Add a manual entry interactively
python listener.py --add

# Regenerate dashboard without fetching new data
python listener.py --dashboard
```

## Architecture

### Core Components

- **`listener.py`** - Main orchestrator (`SocialMediaListener` class). Initializes platform monitors, fetches data, deduplicates posts, and triggers dashboard generation.

- **`dashboard.py`** - Generates a self-contained HTML dashboard with Chart.js visualizations. Entry point: `generate_dashboard(data, output_path)`.

- **`config.py`** - All configuration: API credentials, monitoring targets (channels/accounts/pages), and settings (check interval, storage paths).

### Platform Monitors (`platforms/`)

Each platform module follows the same pattern:
- Factory function `create_monitor(config)` returns a monitor instance
- Monitor has `is_configured()` to check if API credentials exist
- Monitor has fetch methods returning `List[Dict]` of normalized posts

| Module | API | Key Methods |
|--------|-----|-------------|
| `youtube.py` | RSS feeds | `fetch_all_channels()`, `search_videos_for_keywords()` |
| `twitter.py` | X API v2 | `TwitterMonitor.search_recent()`, `.fetch_accounts()` |
| `grok_x.py` | xAI Grok x_search | `GrokXMonitor.search_keywords()`, `.search_accounts()` |
| `meta.py` | Graph API | `MetaMonitor.fetch_all_pages()` |
| `linkedin.py` | LinkedIn API | `LinkedInMonitor.fetch_all_companies()` |
| `manual.py` | Local JSON | `ManualEntryManager.add_entry()`, `.get_all_entries()` |

### Data Flow

1. `SocialMediaListener.fetch_all()` calls each platform monitor
2. Posts are deduplicated by `(platform, id)` tuple
3. Data stored in `social_data.json` (configurable via `DATA_FILE`)
4. `generate_dashboard()` creates `dashboard.html` with embedded Chart.js

### Post Schema

All platform monitors normalize posts to this structure:
```python
{
    "platform": str,      # youtube, twitter, facebook, instagram, linkedin, manual
    "type": str,          # video, tweet, post, etc.
    "id": str,            # unique per platform
    "text": str,          # or "title" for videos
    "url": str,
    "author": str,
    "published": str,     # ISO timestamp
    "fetched_at": str,    # ISO timestamp
    "likes": int,
    "comments": int,
    "shares": int,        # or "retweets" for Twitter
    "views": int,         # optional
}
```

## Adding a New Platform

1. Create `platforms/newplatform.py` with a monitor class
2. Implement `is_configured()` and fetch methods returning normalized posts
3. Add `create_monitor(config)` factory function
4. Add configuration variables to `config.py`
5. Call the monitor from `SocialMediaListener.fetch_all()` in `listener.py`
6. Export from `platforms/__init__.py`

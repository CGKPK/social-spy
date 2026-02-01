# 📊 Social Media Listener

A hybrid social media monitoring tool that aggregates posts from multiple platforms into a beautiful dashboard.

## Features

- **YouTube** - Monitor channels via RSS feeds (no API key required!)
- **X/Twitter** - Track mentions and accounts via API
- **Facebook/Instagram** - Monitor pages you manage via Meta Graph API
- **LinkedIn** - Track company pages via API
- **Manual Entry** - Add posts from any platform manually
- **Beautiful Dashboard** - Interactive HTML report with charts

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Monitoring Targets

Edit `config.py` to add:
- Keywords to monitor
- YouTube channel IDs
- Twitter accounts
- Facebook/Instagram pages
- LinkedIn company pages

### 3. Run the Listener

```bash
# Single run - fetch all and generate dashboard
python listener.py

# Continuous monitoring (checks every 30 minutes)
python listener.py --watch

# Add a post manually
python listener.py --add

# Just regenerate the dashboard
python listener.py --dashboard
```

### 4. View Results

Open `dashboard.html` in your browser to see the interactive dashboard.

## Platform Setup

### YouTube (Works Immediately!)

YouTube monitoring uses RSS feeds - no API key required!

1. Find the channel ID:
   - Go to the channel page
   - View page source and search for "channelId"
   - Or use a tool like [Comment Picker](https://commentpicker.com/youtube-channel-id.php)

2. Add to `config.py`:
```python
YOUTUBE_CHANNELS = [
    {"name": "TED", "channel_id": "UCAuUUnT6oDeKwE6v1US8Lg"},
]
```

### X/Twitter

1. Apply for a developer account at [developer.twitter.com](https://developer.twitter.com/)
2. Create a project and app
3. Generate a Bearer Token
4. Add to `config.py`:
```python
TWITTER_API = {
    "bearer_token": "YOUR_BEARER_TOKEN",
}
```

### Facebook/Instagram (Meta)

1. Create an app at [developers.facebook.com](https://developers.facebook.com/)
2. Add the Pages and Instagram Graph API products
3. Generate a Page Access Token for pages you manage
4. Add to `config.py`:
```python
META_API = {
    "access_token": "YOUR_PAGE_ACCESS_TOKEN",
}

META_PAGES = [
    {"name": "My Page", "page_id": "123456789", "instagram_id": "17841400..."},
]
```

### LinkedIn

1. Create an app at [developer.linkedin.com](https://developer.linkedin.com/)
2. Request Marketing Developer Platform access (for company posts)
3. Generate an OAuth 2.0 Access Token
4. Add to `config.py`:
```python
LINKEDIN_API = {
    "access_token": "YOUR_ACCESS_TOKEN",
}
```

## Manual Entries

For platforms without API access, you can add posts manually:

```bash
python listener.py --add
```

Or programmatically:

```python
from platforms.manual import ManualEntryManager

manager = ManualEntryManager()
manager.add_entry(
    platform="tiktok",
    text="Great video about our product!",
    url="https://tiktok.com/@user/video/123",
    author="@influencer",
    sentiment="positive",
    tags=["product mention", "review"]
)
```

## Dashboard Features

The generated dashboard includes:

- **Stats Overview** - Total posts, likes, comments, shares
- **Platform Distribution** - Doughnut chart showing posts by platform
- **Activity Timeline** - Line chart of posting activity over time
- **Post Feed** - Filterable list of recent posts
- **Top Posts** - Highest-engagement content

## File Structure

```
social_media_listener/
├── config.py          # Configuration and API credentials
├── listener.py        # Main entry point
├── dashboard.py       # HTML dashboard generator
├── requirements.txt   # Python dependencies
├── platforms/
│   ├── youtube.py     # YouTube RSS monitor
│   ├── twitter.py     # X/Twitter API monitor
│   ├── meta.py        # Facebook/Instagram API monitor
│   ├── linkedin.py    # LinkedIn API monitor
│   └── manual.py      # Manual entry manager
├── social_data.json   # Stored post data (auto-generated)
└── dashboard.html     # Generated dashboard (auto-generated)
```

## API Rate Limits

Be mindful of API rate limits:

| Platform | Free Tier Limits |
|----------|-----------------|
| YouTube RSS | No limits (RSS feeds) |
| X/Twitter | 500k tweets/month (Basic) |
| Meta | 200 calls/hour per user |
| LinkedIn | Varies by product |

## Tips

1. **Start with YouTube** - It works immediately without any API setup
2. **Use keywords wisely** - Specific keywords give better results
3. **Run regularly** - Use `--watch` mode for continuous monitoring
4. **Add manual entries** - Don't miss important posts from other platforms
5. **Check the dashboard** - The visual reports make analysis easy

## Troubleshooting

**"API not configured"**
- Check that you've added the correct API credentials in `config.py`

**"No posts found"**
- Verify your channel IDs/page IDs are correct
- Check that the accounts have recent public posts

**Dashboard shows no data**
- Run `python listener.py` first to fetch data
- Check `social_data.json` to see if data was saved

## License

MIT License - feel free to modify and use as needed!

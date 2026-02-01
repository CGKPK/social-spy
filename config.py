"""
Social Media Listener Configuration
====================================
Add your API credentials and monitoring targets here.
"""

# =============================================================================
# MONITORING TARGETS
# =============================================================================

# Keywords to monitor across all platforms
KEYWORDS = [
    # Add your keywords here
    # "your brand name",
    # "your product",
    # "#yourhashag",
]

# YouTube channels to monitor (channel IDs or usernames)
# These work immediately - no API key required!
YOUTUBE_CHANNELS = [
    # Example channels - replace with your own
    {"name": "TED", "channel_id": "UCAuUUnT6oDeKwE6v1US8Lg"},
    {"name": "Veritasium", "channel_id": "UCHnyfMqiRRG1u-2MsSQLbXA"},
]

# X/Twitter accounts to monitor
TWITTER_ACCOUNTS = [
    # "@example_account",
    # "@competitor",
]

# Facebook/Instagram pages to monitor (requires page access)
META_PAGES = [
    # Format: {"name": "Page Name", "page_id": "123456789"}
]

# LinkedIn company pages to monitor
LINKEDIN_COMPANIES = [
    # Format: {"name": "Company Name", "company_id": "company-slug"}
]

# =============================================================================
# API CREDENTIALS
# =============================================================================

# X/Twitter API (https://developer.twitter.com/)
TWITTER_API = {
    "bearer_token": "",  # Your Bearer Token
    "api_key": "",
    "api_secret": "",
    "access_token": "",
    "access_token_secret": "",
}

# Meta Graph API (https://developers.facebook.com/)
META_API = {
    "app_id": "",
    "app_secret": "",
    "access_token": "",  # Page Access Token
}

# LinkedIn API (https://developer.linkedin.com/)
LINKEDIN_API = {
    "client_id": "",
    "client_secret": "",
    "access_token": "",
}

# YouTube Data API (https://console.cloud.google.com/) - Optional for enhanced features
YOUTUBE_API = {
    "api_key": "",  # Optional - RSS feeds work without this
}

# =============================================================================
# SETTINGS
# =============================================================================

# How often to check for new posts (in minutes)
CHECK_INTERVAL = 30

# Maximum posts to store per platform
MAX_POSTS_PER_PLATFORM = 500

# Data storage location
DATA_FILE = "social_data.json"

# Dashboard output location
DASHBOARD_FILE = "dashboard.html"

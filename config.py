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
    "blusky",
    "rules",
    "delayed",
    "payout",
    "price",
    "customer service",
    "propfirm",
    "prop firm",
    "#bluskytrading",
    "#futures",
    "#rithmic",
    "#ninjatrader",
    "#tradovate",
]

# YouTube channels to monitor (channel IDs required)
YOUTUBE_CHANNELS = [
    {"name": "The Futures Desk", "channel_id": "UCUSv1c3-HArVPtFkBCH7Jbw"},
    {"name": "Prop Firm Match", "channel_id": "UCY-imVjtKo8NO4TEEZjh8cw"},
    {"name": "My Funded Futures", "channel_id": "UCBeO1KrgxOjoZCq6MAsYiVA"},
    {"name": "Day Trading Jesus", "channel_id": "UCS5_gAI-iB-aw6_kihiU_FQ"},
    {"name": "Kimmel Trading", "channel_id": "UCQqcRmce3eIAIaAOtNSHrGQ"},
    {"name": "Jason Graystone", "channel_id": "UCCDu1S_OmR5XtM-AzL-_U1Q"},
    {"name": "Kelly Ann Trading", "channel_id": "UCUiQAfFHrTW7LOk29k8DcJA"},
    {"name": "Real Deal Futures", "channel_id": "UC4qtVl1kpaKhNPd_AgeS5Dw"},
    {"name": "Trade Pro", "channel_id": "UCWoWTvvwhfuAqDuxYJHa03Q"},
    {"name": "Mike Swartz", "channel_id": "UCH-_Z7YSk4QTFmXbYSSBB4w"},
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

# xAI Grok API (https://console.x.ai/) - For X/Twitter monitoring via Grok
# Grok has direct real-time access to X data - no separate Twitter API needed!
GROK_API = {
    "api_key": "",  # Add your xAI API key here
}

# X accounts to monitor via Grok (alternative to TWITTER_ACCOUNTS)
GROK_X_ACCOUNTS = [
    "@BluSkyTrading",
    "@saveonpropfirms",
    "@propfirmwise",
    "@onlypropfirms",
    "@FutureswithMike",
    "@FundedNext",
    "@TakeProfitLLC",
    "@Patrickwieland",
]

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

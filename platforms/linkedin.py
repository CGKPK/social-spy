"""
LinkedIn Monitor
==================
Uses the LinkedIn API to monitor company pages you manage.
Requires API credentials from https://developer.linkedin.com/
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional


class LinkedInMonitor:
    """Monitor LinkedIn company pages via API."""

    API_URL = "https://api.linkedin.com/v2"

    def __init__(self, access_token: str):
        """
        Initialize the LinkedIn monitor.

        Args:
            access_token: OAuth 2.0 Access Token with required permissions
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        return bool(self.access_token)

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to the LinkedIn API."""
        try:
            response = requests.get(
                f"{self.API_URL}/{endpoint}",
                headers=self.headers,
                params=params or {}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"❌ LinkedIn API error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ LinkedIn error: {e}")
            return None

    def get_organization_id(self, vanity_name: str) -> Optional[str]:
        """
        Get organization ID from vanity name (company URL slug).

        Args:
            vanity_name: The company's URL slug (e.g., 'microsoft' from linkedin.com/company/microsoft)

        Returns:
            Organization URN or None
        """
        if not self.is_configured():
            return None

        data = self._make_request(
            "organizations",
            {"q": "vanityName", "vanityName": vanity_name}
        )

        if data and "elements" in data and data["elements"]:
            org = data["elements"][0]
            return org.get("id")

        return None

    def get_company_posts(self, organization_id: str, limit: int = 25) -> List[Dict]:
        """
        Get recent posts from a LinkedIn company page.

        Args:
            organization_id: The LinkedIn Organization ID
            limit: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        if not self.is_configured():
            print("⚠️  LinkedIn API not configured - skipping")
            return []

        posts = []

        # Note: This requires Marketing Developer Platform access
        data = self._make_request(
            "shares",
            {
                "q": "owners",
                "owners": f"urn:li:organization:{organization_id}",
                "count": limit,
            }
        )

        if data and "elements" in data:
            for share in data["elements"]:
                content = share.get("content", {})
                text_content = share.get("text", {})

                posts.append({
                    "platform": "linkedin",
                    "type": "post",
                    "id": share.get("id", ""),
                    "text": text_content.get("text", ""),
                    "url": f"https://www.linkedin.com/feed/update/{share.get('activity', '')}",
                    "published": datetime.fromtimestamp(
                        share.get("created", {}).get("time", 0) / 1000
                    ).isoformat() if share.get("created", {}).get("time") else "",
                    "media_type": content.get("contentEntities", [{}])[0].get("entityType", ""),
                    "fetched_at": datetime.now().isoformat(),
                })

        return posts

    def get_company_updates(self, organization_id: str, limit: int = 25) -> List[Dict]:
        """
        Get company updates using the newer Posts API.

        Args:
            organization_id: The LinkedIn Organization ID
            limit: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        if not self.is_configured():
            print("⚠️  LinkedIn API not configured - skipping")
            return []

        posts = []

        # Using the Posts API (requires appropriate permissions)
        data = self._make_request(
            "posts",
            {
                "q": "author",
                "author": f"urn:li:organization:{organization_id}",
                "count": limit,
            }
        )

        if data and "elements" in data:
            for post in data["elements"]:
                posts.append({
                    "platform": "linkedin",
                    "type": "post",
                    "id": post.get("id", ""),
                    "text": post.get("commentary", ""),
                    "url": f"https://www.linkedin.com/feed/update/{post.get('id', '')}",
                    "published": datetime.fromtimestamp(
                        post.get("createdAt", 0) / 1000
                    ).isoformat() if post.get("createdAt") else "",
                    "visibility": post.get("visibility", ""),
                    "fetched_at": datetime.now().isoformat(),
                })

        return posts

    def fetch_all_companies(self, companies: List[Dict]) -> List[Dict]:
        """
        Fetch posts from multiple LinkedIn company pages.

        Args:
            companies: List of company dicts with 'name' and 'company_id' (org ID or vanity name)

        Returns:
            Combined list of posts
        """
        all_posts = []

        for company in companies:
            name = company.get("name", "Unknown")
            company_id = company.get("company_id", "")

            if not company_id:
                print(f"⚠️  Skipping {name}: No company ID provided")
                continue

            print(f"💼 Fetching LinkedIn: {name}...")

            # If it's a vanity name, try to resolve it
            if not company_id.isdigit():
                resolved_id = self.get_organization_id(company_id)
                if resolved_id:
                    company_id = resolved_id
                else:
                    print(f"   Could not resolve company ID for {company_id}")
                    continue

            posts = self.get_company_posts(company_id)
            all_posts.extend(posts)
            print(f"   Found {len(posts)} posts")

        return all_posts


def create_monitor(config: Dict) -> LinkedInMonitor:
    """Create a LinkedIn monitor from config."""
    return LinkedInMonitor(config.get("access_token", ""))


if __name__ == "__main__":
    # Test - requires valid access token
    monitor = LinkedInMonitor("")
    if monitor.is_configured():
        print("LinkedIn API configured - ready to fetch")
    else:
        print("LinkedIn API not configured - add access_token to test")

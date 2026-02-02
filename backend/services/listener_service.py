"""
Service wrapper around the SocialMediaListener.
"""
import sys
import os

# Add parent directory to path to import listener
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from listener import SocialMediaListener
from typing import Dict


class ListenerService:
    """Wrapper service for the SocialMediaListener."""

    def __init__(self):
        """Initialize the listener."""
        self.listener = SocialMediaListener()

    def fetch_once(self) -> Dict[str, int]:
        """
        Run a single fetch operation across all platforms.

        Returns:
            Dictionary with count of new posts per platform
        """
        return self.listener.fetch_all()

    def generate_dashboard(self) -> str:
        """
        Generate the HTML dashboard.

        Returns:
            Path to the generated dashboard file
        """
        return self.listener.generate_report()

    def generate_trends(self) -> str:
        """
        Generate the trend analysis report.

        Returns:
            Path to the generated trend report file
        """
        return self.listener.generate_trends()

    def reload_data(self):
        """Reload data from disk."""
        self.listener.data = self.listener._load_data()

"""
Background monitoring service using asyncio.
"""
import asyncio
from datetime import datetime
from typing import Optional, Dict
from .listener_service import ListenerService


class MonitoringService:
    """Background monitoring service."""

    def __init__(self):
        self._task: Optional[asyncio.Task] = None
        self._status: str = "stopped"
        self._interval: int = 30
        self._last_check: Optional[datetime] = None
        self._listener_service = ListenerService()

    async def start_monitoring(self, interval_minutes: int):
        """
        Start continuous monitoring.

        Args:
            interval_minutes: Minutes between each fetch
        """
        if self._task and not self._task.done():
            raise ValueError("Monitoring is already running")

        self._interval = interval_minutes
        self._status = "running"
        self._task = asyncio.create_task(self._monitoring_loop())

    async def stop_monitoring(self):
        """Stop continuous monitoring."""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        self._status = "stopped"
        self._task = None

    def get_status(self) -> Dict:
        """
        Get current monitoring status.

        Returns:
            Dict with status, last_check, interval_minutes, next_check_in
        """
        next_check_in = None
        if self._status == "running" and self._last_check:
            elapsed = (datetime.now() - self._last_check).total_seconds()
            next_check_in = max(0, int(self._interval * 60 - elapsed))

        return {
            "status": self._status,
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "interval_minutes": self._interval,
            "next_check_in": next_check_in,
        }

    async def _monitoring_loop(self):
        """Internal monitoring loop."""
        while True:
            try:
                # Run fetch in thread pool to avoid blocking
                await asyncio.to_thread(self._run_fetch)
                self._last_check = datetime.now()

                # Sleep until next check
                await asyncio.sleep(self._interval * 60)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                # Continue running even if one fetch fails
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    def _run_fetch(self):
        """Run the fetch operation (blocking)."""
        self._listener_service.fetch_once()


# Global monitoring service instance
monitoring_service = MonitoringService()

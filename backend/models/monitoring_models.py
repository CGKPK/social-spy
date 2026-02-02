"""
Pydantic models for monitoring operations.
"""
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class MonitoringStatus(BaseModel):
    """Monitoring service status."""
    status: str  # "running" | "stopped"
    last_check: Optional[str] = None
    interval_minutes: int
    next_check_in: Optional[int] = None  # seconds until next check


class MonitoringStart(BaseModel):
    """Request to start monitoring."""
    interval_minutes: int = Field(default=30, ge=1, le=1440)


class FetchResults(BaseModel):
    """Results from a fetch operation."""
    results: Dict[str, int]
    total: int
    timestamp: str


class ManualEntryCreate(BaseModel):
    """Create manual entry request."""
    platform: str
    text: str
    author: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[list[str]] = []


class ManualEntryResponse(BaseModel):
    """Manual entry response."""
    id: str
    platform: str
    text: str
    author: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[list[str]] = []
    fetched_at: str

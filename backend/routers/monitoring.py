"""
Monitoring API routes.
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..models.monitoring_models import (
    MonitoringStatus,
    MonitoringStart,
    FetchResults,
)
from ..services.monitoring_service import monitoring_service
from ..services.listener_service import ListenerService

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/status", response_model=MonitoringStatus)
async def get_status():
    """Get current monitoring status."""
    status = monitoring_service.get_status()
    return MonitoringStatus(**status)


@router.post("/start")
async def start_monitoring(request: MonitoringStart):
    """Start continuous monitoring."""
    try:
        await monitoring_service.start_monitoring(request.interval_minutes)
        return {"message": "Monitoring started", "interval_minutes": request.interval_minutes}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stop")
async def stop_monitoring():
    """Stop continuous monitoring."""
    await monitoring_service.stop_monitoring()
    return {"message": "Monitoring stopped"}


@router.post("/fetch", response_model=FetchResults)
async def fetch_now():
    """Trigger a manual fetch immediately."""
    listener = ListenerService()
    results = listener.fetch_once()
    total = sum(results.values())

    return FetchResults(
        results=results,
        total=total,
        timestamp=datetime.now().isoformat(),
    )

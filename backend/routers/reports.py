"""
Reports API routes.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from ..services.listener_service import ListenerService
from ..services.data_service import DataService

router = APIRouter(prefix="/reports", tags=["reports"])
listener_service = ListenerService()
data_service = DataService()


@router.post("/dashboard")
async def generate_dashboard():
    """Generate the HTML dashboard and return the file path."""
    try:
        dashboard_path = listener_service.generate_dashboard()
        return {"message": "Dashboard generated", "path": dashboard_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")


@router.get("/dashboard/file")
async def get_dashboard_file():
    """Download the generated dashboard HTML file."""
    import os
    dashboard_path = "dashboard.html"
    if not os.path.exists(dashboard_path):
        raise HTTPException(status_code=404, detail="Dashboard not found. Generate it first.")
    return FileResponse(dashboard_path, media_type="text/html", filename="dashboard.html")


@router.post("/trends")
async def generate_trends():
    """Generate the trend analysis report."""
    try:
        trends_path = listener_service.generate_trends()
        return {"message": "Trend report generated", "path": trends_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate trends: {str(e)}")


@router.get("/trends/file")
async def get_trends_file():
    """Download the generated trend report markdown file."""
    import os
    trends_path = "trend_report.md"
    if not os.path.exists(trends_path):
        raise HTTPException(status_code=404, detail="Trend report not found. Generate it first.")
    return FileResponse(trends_path, media_type="text/markdown", filename="trend_report.md")


@router.get("/dashboard/data")
async def get_dashboard_data():
    """Get dashboard data as JSON for frontend rendering."""
    try:
        data = data_service.load_posts()
        stats = data_service.get_stats()

        # Get platform distribution
        platform_dist = stats.get("by_platform", {})

        # Get recent activity (last 7 days)
        recent_posts = data_service.get_recent_posts(days=7, limit=100)

        # Group by date for timeline
        from collections import defaultdict
        from datetime import datetime

        timeline = defaultdict(int)
        for post in recent_posts:
            date_str = post.get("published") or post.get("fetched_at", "")
            if date_str:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
                timeline[str(date)] += 1

        return JSONResponse({
            "stats": stats,
            "platform_distribution": platform_dist,
            "timeline": dict(sorted(timeline.items())),
            "total_posts": len(data.get("posts", [])),
            "last_updated": data.get("last_updated"),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard data: {str(e)}")

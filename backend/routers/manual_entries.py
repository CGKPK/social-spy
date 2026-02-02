"""
Manual entries API routes.
"""
import sys
import os
from fastapi import APIRouter, HTTPException
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from platforms.manual import ManualEntryManager
from ..models.monitoring_models import ManualEntryCreate, ManualEntryResponse

router = APIRouter(prefix="/manual", tags=["manual"])
manual_manager = ManualEntryManager()


@router.get("/", response_model=List[ManualEntryResponse])
async def get_entries():
    """Get all manual entries."""
    entries = manual_manager.get_all_entries()
    return [ManualEntryResponse(**entry) for entry in entries]


@router.post("/", response_model=ManualEntryResponse)
async def create_entry(request: ManualEntryCreate):
    """Create a new manual entry."""
    try:
        entry = manual_manager.add_entry(
            platform=request.platform,
            text=request.text,
            author=request.author or "",
            url=request.url or "",
            tags=request.tags or [],
        )
        return ManualEntryResponse(**entry)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create entry: {str(e)}")


@router.post("/bulk")
async def create_bulk_entries(entries: List[ManualEntryCreate]):
    """Create multiple manual entries at once."""
    try:
        entries_data = [
            {
                "platform": e.platform,
                "text": e.text,
                "author": e.author or "",
                "url": e.url or "",
                "tags": e.tags or [],
            }
            for e in entries
        ]
        count = manual_manager.add_bulk(entries_data)
        return {"message": f"{count} entries created", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create entries: {str(e)}")


@router.delete("/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete a manual entry by ID."""
    success = manual_manager.delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry deleted", "id": entry_id}

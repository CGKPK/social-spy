"""
FastAPI Backend for Social Media Listener
==========================================
RESTful API for the social-spy web interface.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import settings
from .middleware.cors import setup_cors
from .routers import (
    monitoring,
    posts,
    config_router,
    manual_entries,
    reports,
)

# Create FastAPI app
app = FastAPI(
    title="Social Media Listener API",
    description="RESTful API for social media monitoring and analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup CORS
setup_cors(app, settings.cors_origins)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "service": "social-media-listener-api",
        "version": "1.0.0",
    })


# Include routers
app.include_router(monitoring.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(config_router.router, prefix="/api")
app.include_router(manual_entries.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Social Media Listener API",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

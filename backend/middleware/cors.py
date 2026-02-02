"""
CORS middleware configuration.
"""
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app, allowed_origins: list[str]):
    """
    Setup CORS middleware for the FastAPI app.

    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed origin URLs
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

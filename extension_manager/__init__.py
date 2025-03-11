"""
Extension Manager for Open WebUI

This extension provides a UI for managing Open WebUI extensions.
"""

import os
import sys
import logging
from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("extension_manager")

# Extension metadata
__id__ = "extension_manager"
__name__ = "Extension Manager"
__description__ = "Manage Open WebUI extensions"
__version__ = "0.1.0"
__author__ = "Open WebUI Team"

# Create router
router = APIRouter(prefix="/api/extensions", tags=["extensions"])

def get_router():
    """Get the extension's API router."""
    # Import extension API
    from .backend.api import setup_routes
    
    # Set up routes
    setup_routes(router)
    
    return router

def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    logger.info("Extension Manager is starting up")
    
    # Register static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount(
            "/extensions/extension_manager/static",
            StaticFiles(directory=static_dir),
            name="extension_manager_static"
        )
        
        logger.info(f"Mounted static files at /extensions/extension_manager/static")
    
    # Add script to inject UI components
    @app.middleware("http")
    async def add_extension_manager_script(request, call_next):
        response = await call_next(request)
        
        # Only modify HTML responses for non-API requests
        if (response.headers.get("content-type", "").startswith("text/html") and
            not request.url.path.startswith("/api/")):
            # Get response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            # Add our script before </body>
            script_tag = f'<script src="/extensions/extension_manager/static/extension_manager.js"></script></body>'
            modified_body = body.replace(b"</body>", script_tag.encode())
            
            # Create new response with modified body
            from starlette.responses import Response
            return Response(
                content=modified_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        return response

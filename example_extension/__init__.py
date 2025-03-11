"""
Example Extension for Open WebUI

This is an example extension that demonstrates how to use the Open WebUI extension framework.
It provides a simple UI dashboard and API endpoints to showcase extension capabilities.

id: example_extension
name: Example Extension
description: Example extension for Open WebUI that demonstrates extension capabilities
version: 0.1.0
author: Open WebUI Team
author_url: https://github.com/open-webui
repository_url: https://github.com/open-webui/extensions
license: MIT
tags: [example, demo, tutorial]
"""

import os
import logging
from fastapi import APIRouter, Request, FastAPI
from starlette.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example_extension")

# Extension metadata
__id__ = "example_extension"
__name__ = "Example Extension"
__description__ = "Example extension for Open WebUI that demonstrates extension capabilities"
__version__ = "0.1.0"
__author__ = "Open WebUI Team"

# Create router
router = APIRouter(prefix="/api/ext/example", tags=["example"])

# Add API routes
@router.get("/hello")
async def hello():
    return {"message": "Hello from Example Extension!"}

@router.get("/counter")
async def get_counter():
    return {"count": 42, "message": "This is an example counter endpoint."}

def get_router():
    """Get the extension's API router."""
    return router

def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    logger.info("Example extension is starting up")
    
    # Register static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount(
            "/extensions/example_extension/static",
            StaticFiles(directory=static_dir),
            name="example_extension_static"
        )
        
        logger.info(f"Mounted static files at /extensions/example_extension/static")
    
    # Add script to inject UI components
    @app.middleware("http")
    async def add_example_script(request, call_next):
        response = await call_next(request)
        
        # Only modify HTML responses for non-API requests
        if (response.headers.get("content-type", "").startswith("text/html") and
            not request.url.path.startswith("/api/")):
            # Get response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            # Add our script before </body>
            script_tag = f'<script src="/extensions/example_extension/static/example.js"></script></body>'
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

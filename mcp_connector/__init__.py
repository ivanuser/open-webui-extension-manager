"""
MCP Connector Extension for Open WebUI

This extension allows connecting to and managing MCP (Model Context Protocol) servers 
directly from the Open WebUI interface.

id: mcp_connector
name: MCP Connector
description: Connect to and manage MCP (Model Context Protocol) servers
version: 0.1.0
author: Open WebUI Team
repository_url: https://github.com/open-webui/extensions
license: MIT
tags: [mcp, models, ai, llm]
"""

import os
import sys
import logging
from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_connector")

# Extension metadata
__id__ = "mcp_connector"
__name__ = "MCP Connector"
__description__ = "Connect to and manage MCP (Model Context Protocol) servers"
__version__ = "0.1.0"
__author__ = "Open WebUI Team"
__repository_url__ = "https://github.com/open-webui/extensions"
__license__ = "MIT"
__tags__ = ["mcp", "models", "ai", "llm"]

# Create router
router = APIRouter(prefix="/api/ext/mcp_connector", tags=["mcp_connector"])

def get_router():
    """Get the extension's API router."""
    # Import API endpoints
    from .api import setup_routes
    
    # Set up routes
    setup_routes(router)
    
    return router

def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    logger.info("MCP Connector is starting up")
    
    # Register static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount(
            "/extensions/mcp_connector/static",
            StaticFiles(directory=static_dir),
            name="mcp_connector_static"
        )
        
        logger.info(f"Mounted static files at /extensions/mcp_connector/static")
    
    # Add script to inject UI components
    @app.middleware("http")
    async def add_mcp_script(request, call_next):
        response = await call_next(request)
        
        # Only modify HTML responses for non-API requests
        if (response.headers.get("content-type", "").startswith("text/html") and
            not request.url.path.startswith("/api/")):
            # Get response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            # Add our script before </body>
            script_tag = f'<script src="/extensions/mcp_connector/static/mcp_manager.js"></script></body>'
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

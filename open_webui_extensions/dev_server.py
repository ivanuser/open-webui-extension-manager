import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import logging
import asyncio

from .extension_system.registry import extension_registry
from .manager.api import create_extension_router
from .manager.ui import ui_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

# Create FastAPI app
app = FastAPI(title="Open WebUI Extension Development Server")

# Add extension API routes
api_router = create_extension_router()
app.include_router(api_router, prefix="/api/extensions")

# Add extension manager UI
app.include_router(ui_router, prefix="/api/_extensions/ui")

# Add static files
static_path = Path(__file__).parent / "manager" / "static"
app.mount("/api/_extensions/static", StaticFiles(directory=str(static_path)), name="extension_static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render the development server home page."""
    extensions = extension_registry.get_all_extensions()
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Open WebUI Extension Development Server</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                margin-top: 0;
            }
            a {
                color: #2196F3;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .links {
                margin-top: 20px;
            }
            .extension-list {
                margin-top: 20px;
            }
            .extension-item {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .extension-name {
                font-weight: bold;
            }
            .extension-description {
                margin-top: 5px;
                color: #666;
            }
            .extension-status {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 12px;
                margin-left: 10px;
            }
            .enabled {
                background-color: #4CAF50;
                color: white;
            }
            .disabled {
                background-color: #f44336;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Open WebUI Extension Development Server</h1>
            <p>Welcome to the Open WebUI Extension Development Server. This server provides a standalone environment for developing and testing extensions for Open WebUI.</p>
            
            <div class="links">
                <h2>Links</h2>
                <ul>
                    <li><a href="/api/_extensions/ui">Extension Manager UI</a></li>
                    <li><a href="/docs">API Documentation</a></li>
                </ul>
            </div>
            
            <div class="extension-list">
                <h2>Installed Extensions</h2>
    """
    
    if not extensions:
        html += "<p>No extensions installed.</p>"
    else:
        for extension_id, extension in extensions.items():
            name = getattr(extension, "name", extension_id)
            description = getattr(extension, "description", "")
            version = getattr(extension, "version", "0.0.0")
            status = "enabled" if extension.enabled else "disabled"
            
            html += f"""
                <div class="extension-item">
                    <div class="extension-name">
                        {name} <span class="extension-status {status}">{status.upper()}</span>
                    </div>
                    <div>Version: {version}</div>
                    <div class="extension-description">{description}</div>
                </div>
            """
    
    html += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)

@app.on_event("startup")
async def startup_event():
    """Initialize the extension system when the development server starts."""
    # Load all extensions
    extension_registry.load_all_extensions()
    
    # Call startup hooks for enabled extensions
    for extension_id, extension in extension_registry.get_all_extensions().items():
        if extension.enabled:
            try:
                await extension.on_startup()
            except Exception as e:
                logger.error(f"Error starting extension {extension_id}: {str(e)}")
    
    logger.info("Extension system initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up the extension system when the development server shuts down."""
    # Call shutdown hooks for enabled extensions
    for extension_id, extension in extension_registry.get_all_extensions().items():
        if extension.enabled:
            try:
                await extension.on_shutdown()
            except Exception as e:
                logger.error(f"Error shutting down extension {extension_id}: {str(e)}")
    
    logger.info("Extension system shut down")

def run_dev_server():
    """Run the development server."""
    uvicorn.run("open_webui_extensions.dev_server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_dev_server()

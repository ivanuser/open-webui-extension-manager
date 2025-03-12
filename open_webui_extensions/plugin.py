from typing import Callable, Dict, List, Any
import logging
import inspect
import asyncio
from pathlib import Path

from .extension_system.base import Extension
from .extension_system.registry import extension_registry
from .extension_system.hooks import hook_manager
from .manager.api import create_extension_router

logger = logging.getLogger("open_webui_extensions")

class OpenWebUIPlugin:
    """Plugin for integrating with Open WebUI."""
    
    def __init__(self):
        self.initialized = False
    
    async def on_startup(self, app):
        """Initialize the extension system when Open WebUI starts."""
        if self.initialized:
            return
        
        try:
            # Load all extensions
            extension_registry.load_all_extensions()
            
            # Register API routes
            api_router = create_extension_router()
            app.include_router(api_router, prefix="/api/extensions")
            
            # Call startup hooks for enabled extensions
            for extension_id, extension in extension_registry.get_all_extensions().items():
                if extension.enabled:
                    try:
                        await extension.on_startup()
                    except Exception as e:
                        logger.error(f"Error starting extension {extension_id}: {str(e)}")
            
            # Add UI routes
            self._add_ui_routes(app)
            
            # Add extension API routes
            self._add_extension_api_routes(app)
            
            self.initialized = True
            logger.info("Extension system initialized")
        
        except Exception as e:
            logger.error(f"Error initializing extension system: {str(e)}")
    
    async def on_shutdown(self, app):
        """Clean up the extension system when Open WebUI shuts down."""
        try:
            # Call shutdown hooks for enabled extensions
            for extension_id, extension in extension_registry.get_all_extensions().items():
                if extension.enabled:
                    try:
                        await extension.on_shutdown()
                    except Exception as e:
                        logger.error(f"Error shutting down extension {extension_id}: {str(e)}")
            
            logger.info("Extension system shut down")
        
        except Exception as e:
            logger.error(f"Error shutting down extension system: {str(e)}")
    
    def _add_ui_routes(self, app):
        """Add UI routes for extensions."""
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from .manager.ui import ui_router
        
        # Add extension manager UI
        app.include_router(ui_router, prefix="/api/_extensions/ui")
        
        # Add static files for extension manager
        static_path = Path(__file__).parent / "manager" / "static"
        app.mount("/api/_extensions/static", StaticFiles(directory=str(static_path)), name="extension_static")
    
    def _add_extension_api_routes(self, app):
        """Add API routes defined by extensions."""
        for extension_id, extension in extension_registry.get_all_extensions().items():
            if extension.enabled and hasattr(extension, "api_routes"):
                for route in extension.api_routes:
                    path = f"/api/extensions/{extension_id}{route['path']}"
                    endpoint = route['endpoint']
                    methods = route['methods']
                    
                    # Register the route
                    for method in methods:
                        app.add_api_route(path, endpoint, methods=[method])

# Create singleton instance
plugin = OpenWebUIPlugin()

# Export the functions for Open WebUI to call
on_startup = plugin.on_startup
on_shutdown = plugin.on_shutdown

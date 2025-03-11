"""
Extension Manager for Open WebUI.

This module provides a management interface for Open WebUI extensions.
"""

import os
import logging
from typing import Dict, Any, Optional, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("extension_manager")

# Import API router
from .backend.api import get_router
from .backend.registry import registry

# Initialize the extension manager
def initialize(config: Optional[Dict[str, Any]] = None) -> bool:
    """Initialize the extension manager.
    
    Args:
        config: Configuration for the extension manager.
        
    Returns:
        True if initialization was successful, False otherwise.
    """
    try:
        # Set up extension directory from config
        extensions_dir = config.get("extensions_dir") if config else None
        registry_config = config.get("registry_config") if config else None
        
        # Initialize the registry
        registry = initialize_registry(extensions_dir, registry_config)
        
        # Discover installed extensions
        extensions = registry.discover()
        logger.info(f"Discovered {len(extensions)} extensions")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing extension manager: {e}")
        return False

def initialize_registry(extensions_dir: Optional[str] = None, registry_config: Optional[str] = None) -> Any:
    """Initialize the extension registry.
    
    Args:
        extensions_dir: The directory containing extensions.
        registry_config: The path to the registry configuration file.
        
    Returns:
        The initialized registry.
    """
    try:
        # Set default extensions directory if not provided
        if not extensions_dir:
            extensions_dir = os.environ.get("EXTENSIONS_DIR", "./extensions")
        
        # Initialize the registry
        from .backend.registry import registry
        registry.__init__(extensions_dir, registry_config)
        
        return registry
    except Exception as e:
        logger.error(f"Error initializing extension registry: {e}")
        raise

def get_api_router() -> Any:
    """Get the API router for the extension manager.
    
    Returns:
        The API router.
    """
    return get_router()

def register_with_app(app: Any, prefix: str = "/api/extensions") -> bool:
    """Register the extension manager with a FastAPI application.
    
    Args:
        app: The FastAPI application.
        prefix: The URL prefix for the extension manager API.
        
    Returns:
        True if registration was successful, False otherwise.
    """
    try:
        # Get the API router
        router = get_api_router()
        
        # Include the router in the application
        app.include_router(router, prefix=prefix)
        
        return True
    except Exception as e:
        logger.error(f"Error registering extension manager with app: {e}")
        return False

def get_ui_mount_points() -> Dict[str, Callable]:
    """Get UI mount points for the extension manager.
    
    Returns:
        A dictionary mapping mount point names to renderer functions.
    """
    try:
        from .frontend import get_mount_points
        return get_mount_points()
    except Exception as e:
        logger.error(f"Error getting UI mount points: {e}")
        return {}

__version__ = "0.1.0"

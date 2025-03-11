"""
Open WebUI Extension Framework

This module provides the framework for creating and managing extensions for Open WebUI.
"""

import os
import sys
import importlib
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui.extensions")

# Extension registry
_extensions = {}

def init_extensions(app: FastAPI) -> None:
    """Initialize all extensions."""
    logger.info("Initializing extensions...")
    
    # Get extensions directory
    extensions_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "extensions")
    if not os.path.exists(extensions_dir):
        logger.warning(f"Extensions directory not found: {extensions_dir}")
        return
    
    # Get extension configuration
    extensions_config = _load_extensions_config()
    
    # Load each enabled extension
    for extension_id, extension_config in extensions_config.items():
        if not extension_config.get("enabled", True):
            logger.info(f"Extension '{extension_id}' is disabled, skipping")
            continue
        
        extension_dir = os.path.join(extensions_dir, extension_id)
        if not os.path.exists(extension_dir):
            logger.warning(f"Extension directory not found: {extension_dir}")
            continue
        
        try:
            # Import the extension module
            sys.path.insert(0, extensions_dir)
            extension_module = importlib.import_module(extension_id)
            sys.path.pop(0)
            
            # Check if the module has a get_router function
            if hasattr(extension_module, "get_router"):
                router = extension_module.get_router()
                app.include_router(router)
                logger.info(f"Registered API routes for extension '{extension_id}'")
            
            # Check if the module has an on_startup function
            if hasattr(extension_module, "on_startup"):
                extension_module.on_startup(app)
                logger.info(f"Called on_startup for extension '{extension_id}'")
            
            # Store the extension module
            _extensions[extension_id] = extension_module
            
            logger.info(f"Initialized extension '{extension_id}'")
        except Exception as e:
            logger.error(f"Error initializing extension '{extension_id}': {e}")
    
    logger.info(f"Initialized {len(_extensions)} extensions")

def _load_extensions_config() -> Dict[str, Dict[str, Any]]:
    """Load the extensions configuration."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "config",
        "extensions.json"
    )
    
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, "r") as f:
                config = json.load(f)
                
                # Convert to dictionary with extension ID as key
                extensions = {}
                for ext in config.get("extensions", []):
                    if "id" in ext:
                        extensions[ext["id"]] = ext
                
                return extensions
        except Exception as e:
            logger.error(f"Error loading extensions config: {e}")
    
    return {}

def get_extension(extension_id: str) -> Optional[Any]:
    """Get an extension module by ID."""
    return _extensions.get(extension_id)

def get_extensions() -> Dict[str, Any]:
    """Get all loaded extensions."""
    return _extensions

# Import base classes and utilities
from .base import (
    BaseExtension, 
    UIExtension, 
    APIExtension,
    ModelExtension,
    ToolExtension,
    ThemeExtension,
    ExtensionContext,
    ExtensionMetadata
)

# Import decorators
from .decorators import (
    hook,
    api_route,
    admin_page,
    sidebar_item,
    settings_section
)

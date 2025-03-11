"""
Utility functions for Open WebUI extensions.
"""

import os
import sys
import importlib
import logging
import inspect
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui.extensions.utils")


def get_extensions_dir() -> str:
    """Get the extensions directory."""
    # Try to use environment variable
    if "OPEN_WEBUI_EXTENSIONS_DIR" in os.environ:
        return os.environ["OPEN_WEBUI_EXTENSIONS_DIR"]
    
    # Try to use Open WebUI config
    try:
        from open_webui.config import EXTENSIONS_DIR
        return EXTENSIONS_DIR
    except ImportError:
        pass
    
    # Default location
    root_dir = os.environ.get("OPEN_WEBUI_ROOT", os.getcwd())
    return os.path.join(root_dir, "extensions")


def extract_metadata_from_docstring(docstring: str) -> Dict[str, Any]:
    """Extract metadata from a docstring."""
    metadata = {}
    
    if not docstring:
        return metadata
    
    # Parse key-value pairs from docstring
    lines = docstring.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if ": " in line:
            key, value = line.split(": ", 1)
            metadata[key.lower()] = value
    
    return metadata


def load_extension_module(extension_id: str, extension_dir: str) -> Optional[Any]:
    """Load an extension module from a directory."""
    try:
        # Add the parent directory to sys.path temporarily
        parent_dir = os.path.dirname(extension_dir)
        sys.path.insert(0, parent_dir)
        
        # Import the module
        module = importlib.import_module(extension_id)
        
        # Remove the parent directory from sys.path
        sys.path.pop(0)
        
        return module
    
    except Exception as e:
        logger.error(f"Error loading extension module '{extension_id}': {e}")
        return None


def get_extension_metadata(extension_id: str, module: Any) -> Dict[str, Any]:
    """Get extension metadata from a module."""
    metadata = {}
    
    # Start with default values
    metadata["id"] = extension_id
    metadata["name"] = extension_id
    metadata["description"] = ""
    metadata["version"] = "0.1.0"
    metadata["author"] = "Unknown"
    
    # Extract metadata from docstring
    if module.__doc__:
        docstring_metadata = extract_metadata_from_docstring(module.__doc__)
        metadata.update(docstring_metadata)
    
    # Extract metadata from module variables
    for key in ["id", "name", "description", "version", "author",
               "author_url", "repository_url", "license", "tags", "requires"]:
        if hasattr(module, f"__{key}__"):
            value = getattr(module, f"__{key}__")
            if value is not None:
                metadata[key] = value
    
    return metadata


def find_extension_class(module: Any) -> Optional[Any]:
    """Find an extension class in a module."""
    try:
        from .base import BaseExtension
        
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, BaseExtension) and
                obj is not BaseExtension and obj.__module__ == module.__name__):
                return obj
        
        return None
    
    except Exception as e:
        logger.error(f"Error finding extension class: {e}")
        return None

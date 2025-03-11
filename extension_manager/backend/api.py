"""
API endpoints for the Extension Manager.

This module provides the API endpoints for managing extensions in Open WebUI.
"""

import os
import sys
import json
import logging
import tempfile
import shutil
import zipfile
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from .registry import ExtensionRegistry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("extension_manager.api")

# Models
class Extension(BaseModel):
    """Model for an extension."""
    id: str
    name: str
    description: str
    version: str
    author: str
    author_url: Optional[str] = None
    repository_url: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    enabled: bool = True
    installed_at: str
    updated_at: str
    path: str
    config: Dict[str, Any] = {}

class ExtensionList(BaseModel):
    """Model for a list of extensions."""
    extensions: List[Extension]

class ExtensionToggle(BaseModel):
    """Model for toggling an extension."""
    enable: Optional[bool] = None

class ExtensionResponse(BaseModel):
    """Model for an extension response."""
    success: bool
    message: str
    extension: Optional[Extension] = None

# Initialize extension registry
registry = None

def get_extension_registry():
    """Get the extension registry."""
    global registry
    if registry is None:
        # Get the Open WebUI root directory
        root_dir = os.environ.get("OPEN_WEBUI_ROOT", os.getcwd())
        registry = ExtensionRegistry(root_dir)
    return registry

def setup_routes(router: APIRouter):
    """Set up API routes for the Extension Manager."""
    
    @router.get("/", response_model=ExtensionList)
    async def get_extensions():
        """Get all installed extensions."""
        registry = get_extension_registry()
        extensions = registry.get_extensions()
        return ExtensionList(extensions=extensions)
    
    @router.get("/{extension_id}", response_model=Extension)
    async def get_extension(extension_id: str):
        """Get an extension by ID."""
        registry = get_extension_registry()
        extension = registry.get_extension_by_id(extension_id)
        
        if not extension:
            raise HTTPException(
                status_code=404,
                detail=f"Extension '{extension_id}' not found"
            )
        
        return extension
    
    @router.post("/install", response_model=ExtensionResponse)
    async def install_extension(file: UploadFile = File(...)):
        """Install an extension from a ZIP file."""
        registry = get_extension_registry()
        
        # Check if file is a ZIP file
        if not file.filename.endswith(".zip"):
            raise HTTPException(
                status_code=400,
                detail="Extension package must be a ZIP file"
            )
        
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save the uploaded file
                temp_file = os.path.join(temp_dir, file.filename)
                with open(temp_file, "wb") as f:
                    content = await file.read()
                    f.write(content)
                
                # Extract the zip file
                with zipfile.ZipFile(temp_file, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the extension directory
                extension_dir = None
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                        extension_dir = item_path
                        break
                
                if not extension_dir:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid extension package. No extension directory found."
                    )
                
                # Install the extension
                extension = registry.install_extension(extension_dir)
                
                return ExtensionResponse(
                    success=True,
                    message=f"Extension '{extension.name}' installed successfully.",
                    extension=extension
                )
        
        except Exception as e:
            logger.error(f"Error installing extension: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error installing extension: {str(e)}"
            )
    
    @router.post("/{extension_id}/toggle", response_model=ExtensionResponse)
    async def toggle_extension(extension_id: str, toggle: ExtensionToggle):
        """Enable or disable an extension."""
        registry = get_extension_registry()
        
        # Check if extension exists
        extension = registry.get_extension_by_id(extension_id)
        if not extension:
            raise HTTPException(
                status_code=404,
                detail=f"Extension '{extension_id}' not found"
            )
        
        # Determine the new enabled state
        enabled = not extension.enabled if toggle.enable is None else toggle.enable
        
        # Toggle the extension
        updated_extension = registry.toggle_extension(extension_id, enabled)
        
        return ExtensionResponse(
            success=True,
            message=f"Extension '{extension_id}' {'enabled' if enabled else 'disabled'} successfully.",
            extension=updated_extension
        )
    
    @router.delete("/{extension_id}", response_model=ExtensionResponse)
    async def delete_extension(extension_id: str):
        """Delete an extension."""
        registry = get_extension_registry()
        
        # Check if extension exists
        extension = registry.get_extension_by_id(extension_id)
        if not extension:
            raise HTTPException(
                status_code=404,
                detail=f"Extension '{extension_id}' not found"
            )
        
        # Don't allow deleting the extension manager itself
        if extension_id == "extension_manager":
            raise HTTPException(
                status_code=400,
                detail="Cannot delete the Extension Manager itself."
            )
        
        # Delete the extension
        success = registry.delete_extension(extension_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting extension '{extension_id}'"
            )
        
        return ExtensionResponse(
            success=True,
            message=f"Extension '{extension_id}' deleted successfully."
        )

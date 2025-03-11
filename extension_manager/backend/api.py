"""
API endpoints for the Extension Manager.

This module provides the API endpoints for managing extensions in Open WebUI.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
import logging

from .models import (
    ExtensionInfo,
    ExtensionStatus,
    ExtensionType,
    ExtensionSource,
    ExtensionAction,
    ExtensionInstall,
    ExtensionSettings,
    ExtensionList,
    ExtensionFilters,
    ExtensionActionResponse,
    ExtensionListResponse,
)

from .registry import registry

router = APIRouter(prefix="/api/extensions", tags=["extensions"])

logger = logging.getLogger("extension_api")

@router.get("/", response_model=ExtensionListResponse)
async def list_extensions(
    types: List[ExtensionType] = Query(None),
    status: List[ExtensionStatus] = Query(None),
    sources: List[ExtensionSource] = Query(None),
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """List all extensions."""
    try:
        # Create filters
        filters = ExtensionFilters(
            types=types,
            status=status,
            sources=sources,
            search=search,
        )
        
        # Get extensions from registry
        extensions = registry.list_extensions(filters)
        
        # Paginate results
        total = len(extensions)
        start = (page - 1) * page_size
        end = start + page_size
        extensions = extensions[start:end]
        
        return ExtensionListResponse(
            success=True,
            message=f"Found {total} extensions",
            extensions=extensions,
            total=total,
            page=page,
            page_size=page_size,
            filters=filters,
        )
    except Exception as e:
        logger.error(f"Error listing extensions: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing extensions: {e}")

@router.get("/{name}", response_model=ExtensionActionResponse)
async def get_extension(name: str):
    """Get information about an extension."""
    try:
        # Get extension info
        ext_info = registry.get_extension_info(name)
        
        if not ext_info:
            return ExtensionActionResponse(
                success=False,
                message=f"Extension {name} not found",
            )
        
        return ExtensionActionResponse(
            success=True,
            message=f"Extension {name} found",
            extension=ext_info,
        )
    except Exception as e:
        logger.error(f"Error getting extension {name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting extension: {e}")

@router.post("/install", response_model=ExtensionActionResponse)
async def install_extension(install_info: ExtensionInstall):
    """Install an extension."""
    try:
        # Install the extension
        success, ext_info, message = registry.install_extension(
            source=install_info.source,
            url=install_info.url,
            path=install_info.path,
            name=install_info.name,
        )
        
        return ExtensionActionResponse(
            success=success,
            message=message,
            extension=ext_info,
        )
    except Exception as e:
        logger.error(f"Error installing extension: {e}")
        raise HTTPException(status_code=500, detail=f"Error installing extension: {e}")

@router.post("/action", response_model=ExtensionActionResponse)
async def extension_action(action_info: ExtensionAction):
    """Perform an action on an extension."""
    try:
        # Get extension info
        ext_info = registry.get_extension_info(action_info.name)
        
        if not ext_info:
            return ExtensionActionResponse(
                success=False,
                message=f"Extension {action_info.name} not found",
            )
        
        # Perform the action
        if action_info.action == "enable":
            success, message = registry.enable_extension(action_info.name)
        elif action_info.action == "disable":
            success, message = registry.disable_extension(action_info.name)
        elif action_info.action == "uninstall":
            success, message = registry.uninstall_extension(action_info.name)
        else:
            return ExtensionActionResponse(
                success=False,
                message=f"Unknown action: {action_info.action}",
                extension=ext_info,
            )
        
        # Get updated extension info if the action was successful
        if success and action_info.action != "uninstall":
            ext_info = registry.get_extension_info(action_info.name)
        
        return ExtensionActionResponse(
            success=success,
            message=message,
            extension=ext_info if action_info.action != "uninstall" else None,
        )
    except Exception as e:
        logger.error(f"Error performing action {action_info.action} on extension {action_info.name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error performing action: {e}")

@router.post("/settings", response_model=ExtensionActionResponse)
async def update_settings(settings_info: ExtensionSettings):
    """Update extension settings."""
    try:
        # Get extension info
        ext_info = registry.get_extension_info(settings_info.name)
        
        if not ext_info:
            return ExtensionActionResponse(
                success=False,
                message=f"Extension {settings_info.name} not found",
            )
        
        # Update settings
        success, message = registry.update_extension_settings(
            settings_info.name,
            settings_info.settings,
        )
        
        # Get updated extension info
        if success:
            ext_info = registry.get_extension_info(settings_info.name)
        
        return ExtensionActionResponse(
            success=success,
            message=message,
            extension=ext_info,
        )
    except Exception as e:
        logger.error(f"Error updating settings for extension {settings_info.name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating settings: {e}")

@router.post("/discover", response_model=ExtensionListResponse)
async def discover_extensions():
    """Discover installed extensions."""
    try:
        # Discover extensions
        extensions = registry.discover()
        
        return ExtensionListResponse(
            success=True,
            message=f"Discovered {len(extensions)} extensions",
            extensions=list(extensions.values()),
            total=len(extensions),
            page=1,
            page_size=len(extensions),
        )
    except Exception as e:
        logger.error(f"Error discovering extensions: {e}")
        raise HTTPException(status_code=500, detail=f"Error discovering extensions: {e}")

@router.post("/initialize", response_model=Dict[str, Any])
async def initialize_extensions():
    """Initialize all extensions."""
    try:
        # Initialize extensions
        results = registry.initialize_all()
        
        # Count successes and failures
        successes = sum(1 for success, _ in results.values() if success)
        failures = len(results) - successes
        
        return {
            "success": failures == 0,
            "message": f"Initialized {successes} extensions successfully, {failures} failed",
            "results": {name: {"success": success, "message": message} for name, (success, message) in results.items()},
        }
    except Exception as e:
        logger.error(f"Error initializing extensions: {e}")
        raise HTTPException(status_code=500, detail=f"Error initializing extensions: {e}")

def get_router() -> APIRouter:
    """Get the API router."""
    return router

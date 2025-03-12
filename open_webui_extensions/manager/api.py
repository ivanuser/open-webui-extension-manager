from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import os
import tempfile
import shutil
import zipfile
import logging

from ..extension_system.registry import extension_registry

logger = logging.getLogger("open_webui_extensions")

def create_extension_router():
    """Create and return the extension API router."""
    router = APIRouter()
    
    @router.get("/")
    async def list_extensions():
        """List all installed extensions."""
        extensions = extension_registry.get_all_extensions()
        
        result = []
        for extension_id, extension in extensions.items():
            result.append({
                "id": extension_id,
                "name": getattr(extension, "name", extension_id),
                "description": getattr(extension, "description", ""),
                "version": getattr(extension, "version", "0.0.0"),
                "author": getattr(extension, "author", ""),
                "enabled": extension.enabled,
                "installed": extension.installed,
            })
        
        return result
    
    @router.get("/{extension_id}")
    async def get_extension(extension_id: str):
        """Get details for a specific extension."""
        extension = extension_registry.get_extension(extension_id)
        
        if not extension:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        return {
            "id": extension_id,
            "name": getattr(extension, "name", extension_id),
            "description": getattr(extension, "description", ""),
            "version": getattr(extension, "version", "0.0.0"),
            "author": getattr(extension, "author", ""),
            "enabled": extension.enabled,
            "installed": extension.installed,
        }
    
    @router.post("/{extension_id}/enable")
    async def enable_extension(extension_id: str):
        """Enable an extension."""
        success = extension_registry.enable_extension(extension_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        # Get the extension
        extension = extension_registry.get_extension(extension_id)
        
        # Call the startup hook
        try:
            await extension.on_startup()
        except Exception as e:
            logger.error(f"Error starting extension {extension_id}: {str(e)}")
            return JSONResponse(status_code=500, content={"detail": str(e)})
        
        return {"status": "success"}
    
    @router.post("/{extension_id}/disable")
    async def disable_extension(extension_id: str):
        """Disable an extension."""
        # Get the extension
        extension = extension_registry.get_extension(extension_id)
        
        if not extension:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        # Call the shutdown hook
        try:
            await extension.on_shutdown()
        except Exception as e:
            logger.error(f"Error shutting down extension {extension_id}: {str(e)}")
        
        # Disable the extension
        success = extension_registry.disable_extension(extension_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        return {"status": "success"}
    
    @router.post("/install")
    async def install_extension(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        extension_id: Optional[str] = Form(None)
    ):
        """Install an extension from a ZIP file."""
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            zip_path = os.path.join(temp_dir, file.filename)
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            
            # Extract the ZIP file
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail="Invalid ZIP file")
            
            # Find the extension directory
            # The extension should be in a subdirectory with an __init__.py file
            extension_dir = None
            for root, dirs, files in os.walk(extract_dir):
                if "__init__.py" in files:
                    extension_dir = root
                    break
            
            if not extension_dir:
                raise HTTPException(status_code=400, detail="No valid extension found in ZIP file")
            
            # Install the extension
            result = extension_registry.install_extension(extension_dir, extension_id)
            
            if not result:
                raise HTTPException(status_code=500, detail="Failed to install extension")
            
            return {"status": "success", "extension_id": result}
    
    @router.delete("/{extension_id}")
    async def uninstall_extension(extension_id: str):
        """Uninstall an extension."""
        success = extension_registry.uninstall_extension(extension_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        return {"status": "success"}
    
    @router.get("/{extension_id}/settings")
    async def get_extension_settings(extension_id: str):
        """Get settings for a specific extension."""
        extension = extension_registry.get_extension(extension_id)
        
        if not extension:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        return extension.get_settings()
    
    @router.post("/{extension_id}/settings")
    async def update_extension_settings(extension_id: str, settings: Dict[str, Any]):
        """Update settings for a specific extension."""
        extension = extension_registry.get_extension(extension_id)
        
        if not extension:
            raise HTTPException(status_code=404, detail=f"Extension {extension_id} not found")
        
        extension.update_settings(settings)
        
        return {"status": "success"}
    
    return router

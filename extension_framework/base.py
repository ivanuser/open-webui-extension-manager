"""
Base classes for Open WebUI extensions.
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar
from pathlib import Path

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui.extensions")

# Type definitions
T = TypeVar('T')


class ExtensionMetadata(BaseModel):
    """Metadata for an extension."""
    id: str
    name: str
    description: str
    version: str
    author: str
    author_url: Optional[str] = None
    repository_url: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    requires: List[str] = []


class ExtensionContext:
    """Context for an extension."""
    def __init__(self, extension_id: str, extension_path: str):
        self.id = extension_id
        self.path = extension_path
        self.static_path = os.path.join(extension_path, "static")
        self.config_path = os.path.join(extension_path, "config")
        self.data_path = os.path.join(extension_path, "data")
        self.temp_path = os.path.join(extension_path, "temp")
        
        # Create directories
        os.makedirs(self.static_path, exist_ok=True)
        os.makedirs(self.config_path, exist_ok=True)
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)
        
        # Config cache
        self._config_cache = {}
    
    def get_config(self, name: str = "config") -> Dict[str, Any]:
        """Get a configuration file."""
        if name in self._config_cache:
            return self._config_cache[name]
        
        config_file = os.path.join(self.config_path, f"{name}.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    self._config_cache[name] = config
                    return config
            except Exception as e:
                logger.error(f"Error loading config {name}: {e}")
                return {}
        else:
            return {}
    
    def save_config(self, config: Dict[str, Any], name: str = "config") -> bool:
        """Save a configuration file."""
        try:
            config_file = os.path.join(self.config_path, f"{name}.json")
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)
            self._config_cache[name] = config
            return True
        except Exception as e:
            logger.error(f"Error saving config {name}: {e}")
            return False
    
    def get_static_url(self, path: str) -> str:
        """Get the URL for a static file."""
        return f"/extensions/{self.id}/static/{path}"


class BaseExtension:
    """Base class for extensions."""
    
    # Class variables
    id: str = None
    name: str = None
    description: str = None
    version: str = "0.1.0"
    author: str = None
    author_url: Optional[str] = None
    repository_url: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    requires: List[str] = []
    
    def __init__(self, context: ExtensionContext):
        """Initialize the extension."""
        if not self.id:
            raise ValueError("Extension ID is required")
        
        self.context = context
        self.router = APIRouter(prefix=f"/api/ext/{self.id}", tags=[self.id])
        self.logger = logging.getLogger(f"open_webui.extensions.{self.id}")
    
    def get_metadata(self) -> ExtensionMetadata:
        """Get the extension metadata."""
        return ExtensionMetadata(
            id=self.id,
            name=self.name or self.id,
            description=self.description or "",
            version=self.version,
            author=self.author or "Unknown",
            author_url=self.author_url,
            repository_url=self.repository_url,
            license=self.license,
            tags=self.tags,
            requires=self.requires
        )
    
    def get_router(self) -> APIRouter:
        """Get the API router."""
        return self.router
    
    async def on_startup(self, app: FastAPI) -> None:
        """Called when the extension starts up."""
        pass
    
    async def on_shutdown(self, app: FastAPI) -> None:
        """Called when the extension shuts down."""
        pass
    
    async def register_routes(self, app: FastAPI) -> None:
        """Register API routes with the application."""
        app.include_router(self.router)
    
    async def register_ui(self, app: FastAPI) -> None:
        """Register UI components with the application."""
        pass


class UIExtension(BaseExtension):
    """Extension that provides UI components."""
    
    # UI component entry points
    admin_page: Optional[Dict[str, str]] = None
    sidebar_items: List[Dict[str, str]] = []
    settings_sections: List[Dict[str, str]] = []
    
    async def register_ui(self, app: FastAPI) -> None:
        """Register UI components with the application."""
        await super().register_ui(app)
        
        # Register static files
        if os.path.exists(self.context.static_path):
            from starlette.staticfiles import StaticFiles
            app.mount(
                f"/extensions/{self.id}/static",
                StaticFiles(directory=self.context.static_path),
                name=f"{self.id}_static"
            )
            
            self.logger.info(f"Mounted static files at /extensions/{self.id}/static")


class APIExtension(BaseExtension):
    """Extension that provides API endpoints."""
    pass


class ModelExtension(BaseExtension):
    """Extension that provides model adapters."""
    
    # Model information
    models: List[Dict[str, Any]] = []
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models."""
        return self.models
    
    async def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        for model in self.models:
            if model.get("id") == model_id:
                return model
        return None


class ToolExtension(BaseExtension):
    """Extension that provides tools."""
    
    # Tool information
    tools: List[Dict[str, Any]] = []
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        return self.tools
    
    async def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool."""
        raise NotImplementedError(f"Tool execution not implemented for {tool_id}")


class ThemeExtension(BaseExtension):
    """Extension that provides themes."""
    
    # Theme information
    themes: List[Dict[str, Any]] = []
    
    async def list_themes(self) -> List[Dict[str, Any]]:
        """List available themes."""
        return self.themes
    
    async def get_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific theme."""
        for theme in self.themes:
            if theme.get("id") == theme_id:
                return theme
        return None

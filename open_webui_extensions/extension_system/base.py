from typing import Dict, List, Optional, Any, Callable, Type
import importlib
import inspect
import os
import sys
import logging

logger = logging.getLogger("open_webui_extensions")

class Extension:
    """Base class for all extensions."""
    
    # Extension metadata
    id: str = None
    name: str = None
    description: str = None
    version: str = None
    author: str = None
    
    # Extension state
    enabled: bool = False
    installed: bool = False
    path: str = None
    
    # Extension hooks
    hooks: Dict[str, List[Callable]] = {}
    
    def __init__(self):
        if not self.id:
            self.id = self.__class__.__module__
        
        # Initialize empty hook lists
        if not hasattr(self, 'hooks') or not self.hooks:
            self.hooks = {
                'on_startup': [],
                'on_shutdown': [],
                'on_chat_request': [],
                'on_chat_response': [],
                'on_ui_tab': [],
                'on_api_route': [],
                'on_tool': [],
            }
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a callback for a specific hook."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
    
    async def on_startup(self) -> None:
        """Called when the extension is started."""
        for hook in self.hooks.get('on_startup', []):
            await hook()
    
    async def on_shutdown(self) -> None:
        """Called when the extension is stopped."""
        for hook in self.hooks.get('on_shutdown', []):
            await hook()
    
    def get_settings(self) -> Dict[str, Any]:
        """Get extension settings."""
        return {}
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update extension settings."""
        pass

class UIExtension(Extension):
    """Extension that adds UI components to Open WebUI."""
    
    ui_components: List[Dict[str, Any]] = []
    
    def register_ui_component(self, location: str, component: Dict[str, Any]) -> None:
        """Register a UI component."""
        self.ui_components.append({
            'location': location,
            'component': component,
        })

class APIExtension(Extension):
    """Extension that adds API endpoints to Open WebUI."""
    
    api_routes: List[Dict[str, Any]] = []
    
    def register_api_route(self, path: str, endpoint: Callable, methods: List[str] = ["GET"]) -> None:
        """Register an API endpoint."""
        self.api_routes.append({
            'path': path,
            'endpoint': endpoint,
            'methods': methods,
        })

class ModelAdapterExtension(Extension):
    """Extension that adds a new model adapter to Open WebUI."""
    
    async def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate a completion using the model."""
        raise NotImplementedError("Subclasses must implement generate_completion")

class ToolExtension(Extension):
    """Extension that adds new tools to Open WebUI."""
    
    tools: List[Dict[str, Any]] = []
    
    def register_tool(self, name: str, description: str, function: Callable) -> None:
        """Register a tool."""
        self.tools.append({
            'name': name,
            'description': description,
            'function': function,
        })

class ThemeExtension(Extension):
    """Extension that adds a new theme to Open WebUI."""
    
    css_path: str = None
    js_path: str = None

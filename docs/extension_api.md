# Extension API Reference

This document provides a reference for the Extension API in Open WebUI.

## Core Classes

### BaseExtension

The base class for all extensions.

```python
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
        pass
    
    def get_metadata(self) -> ExtensionMetadata:
        """Get the extension metadata."""
        pass
    
    def get_router(self) -> APIRouter:
        """Get the API router."""
        pass
    
    async def on_startup(self, app: FastAPI) -> None:
        """Called when the extension starts up."""
        pass
    
    async def on_shutdown(self, app: FastAPI) -> None:
        """Called when the extension shuts down."""
        pass
    
    async def register_routes(self, app: FastAPI) -> None:
        """Register API routes with the application."""
        pass
    
    async def register_ui(self, app: FastAPI) -> None:
        """Register UI components with the application."""
        pass
```

### UIExtension

Extension that provides UI components.

```python
class UIExtension(BaseExtension):
    """Extension that provides UI components."""
    
    # UI component entry points
    admin_page: Optional[str] = None
    sidebar_items: List[Dict[str, str]] = []
    settings_sections: List[Dict[str, str]] = []
    
    async def register_ui(self, app: FastAPI) -> None:
        """Register UI components with the application."""
        pass
```

### APIExtension

Extension that provides API endpoints.

```python
class APIExtension(BaseExtension):
    """Extension that provides API endpoints."""
    pass
```

### ModelExtension

Extension that provides model adapters.

```python
class ModelExtension(BaseExtension):
    """Extension that provides model adapters."""
    
    # Model information
    models: List[Dict[str, Any]] = []
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models."""
        pass
    
    async def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        pass
```

### ToolExtension

Extension that provides tools.

```python
class ToolExtension(BaseExtension):
    """Extension that provides tools."""
    
    # Tool information
    tools: List[Dict[str, Any]] = []
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        pass
    
    async def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Any:
        """Execute a tool."""
        pass
```

### ThemeExtension

Extension that provides themes.

```python
class ThemeExtension(BaseExtension):
    """Extension that provides themes."""
    
    # Theme information
    themes: List[Dict[str, Any]] = []
    
    async def list_themes(self) -> List[Dict[str, Any]]:
        """List available themes."""
        pass
    
    async def get_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific theme."""
        pass
```

## Extension Context

The `ExtensionContext` class provides access to extension-specific directories and configuration.

```python
class ExtensionContext:
    """Context for an extension."""
    def __init__(self, extension_id: str, extension_path: str):
        self.id = extension_id
        self.path = extension_path
        self.static_path = os.path.join(extension_path, "static")
        self.config_path = os.path.join(extension_path, "config")
        self.data_path = os.path.join(extension_path, "data")
        self.temp_path = os.path.join(extension_path, "temp")
    
    def get_config(self, name: str = "config") -> Dict[str, Any]:
        """Get a configuration file."""
        pass
    
    def save_config(self, config: Dict[str, Any], name: str = "config") -> bool:
        """Save a configuration file."""
        pass
    
    def get_static_url(self, path: str) -> str:
        """Get the URL for a static file."""
        pass
```

## Decorators

### @hook

Register a hook callback.

```python
@hook("app_startup")
def startup_hook(app):
    """Hook that runs at application startup."""
    pass
```

### @api_route

Register an API route.

```python
@api_route("/hello", methods=["GET"])
async def hello():
    """Hello endpoint."""
    return {"message": "Hello!"}
```

### @admin_page

Register an admin page.

```python
@admin_page(title="My Extension", icon="puzzle-piece", path="/admin/myext")
class MyExtension(UIExtension):
    pass
```

### @sidebar_item

Register a sidebar item.

```python
@sidebar_item(title="My Feature", icon="star", path="/myfeature")
class MyExtension(UIExtension):
    pass
```

### @settings_section

Register a settings section.

```python
@settings_section(title="My Settings", icon="cog", component="my-settings")
class MyExtension(UIExtension):
    pass
```

## Extension Manager API

### GET /api/extensions/

Get all installed extensions.

### GET /api/extensions/{extension_id}

Get an extension by ID.

### POST /api/extensions/install

Install an extension from a zip file.

### POST /api/extensions/{extension_id}/toggle

Enable or disable an extension.

### DELETE /api/extensions/{extension_id}

Delete an extension.

## Extension Metadata

Extensions can include metadata in their `__init__.py` file:

```python
"""
My Extension for Open WebUI

id: my_extension
name: My Extension
description: A custom extension for Open WebUI
version: 0.1.0
author: Your Name
author_url: https://example.com
repository_url: https://github.com/your-username/my-extension
license: MIT
tags: [example, demo]
requires: [another_extension]
"""
```

Alternatively, you can use class variables:

```python
class MyExtension(UIExtension):
    id = "my_extension"
    name = "My Extension"
    description = "A custom extension for Open WebUI"
    version = "0.1.0"
    author = "Your Name"
    author_url = "https://example.com"
    repository_url = "https://github.com/your-username/my-extension"
    license = "MIT"
    tags = ["example", "demo"]
    requires = ["another_extension"]
```

## Hooks

Hooks allow extensions to integrate with various parts of Open WebUI:

- `app_startup`: Called when the application starts up
- `app_shutdown`: Called when the application shuts down
- `before_request`: Called before each request
- `after_request`: Called after each request
- `message_received`: Called when a message is received
- `message_sent`: Called when a message is sent
- `model_loaded`: Called when a model is loaded

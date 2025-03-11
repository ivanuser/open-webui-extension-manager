# Creating Extensions for Open WebUI

This guide will walk you through the process of creating extensions for Open WebUI.

## Table of Contents

- [Extension Structure](#extension-structure)
- [Extension Types](#extension-types)
- [Extension Base Class](#extension-base-class)
- [Using Hooks](#using-hooks)
- [Creating UI Components](#creating-ui-components)
- [Adding API Endpoints](#adding-api-endpoints)
- [Configuring Settings](#configuring-settings)
- [Packaging Extensions](#packaging-extensions)
- [Example Extension](#example-extension)

## Extension Structure

An extension is a Python package with a specific structure:

```
my-extension/
├── __init__.py        # Main extension entry point
├── ui.py              # UI components
├── api.py             # API endpoints
└── static/            # Static assets
    ├── styles.css
    └── scripts.js
```

The `__init__.py` file is the main entry point for your extension. It should define a class that inherits from one of the extension base classes and create an instance of it.

## Extension Types

Open WebUI supports several types of extensions:

- **UI Extensions**: Add new UI components to Open WebUI
- **API Extensions**: Add new API endpoints
- **Model Adapters**: Integrate new AI models
- **Tool Extensions**: Add new tools or capabilities
- **Theme Extensions**: Customize the appearance

Each type has its own base class that provides specific functionality.

## Extension Base Class

All extensions must inherit from the `Extension` base class or one of its subclasses. Here's a basic example:

```python
from extension_framework import Extension

class MyExtension(Extension):
    @property
    def name(self) -> str:
        return "my-extension"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    @property
    def description(self) -> str:
        return "My awesome extension for Open WebUI."
    
    @property
    def author(self) -> str:
        return "Your Name"
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the extension."""
        return True
    
    def activate(self) -> bool:
        """Activate the extension."""
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension."""
        return True

# Create an instance of the extension
extension = MyExtension()
```

The `Extension` base class requires you to implement several properties:

- `name`: A unique identifier for your extension
- `version`: The version of your extension
- `description`: A description of what your extension does
- `author`: The author of your extension

You should also implement the following methods:

- `initialize`: Called when the extension is first loaded
- `activate`: Called when the extension is enabled
- `deactivate`: Called when the extension is disabled

## Using Hooks

Hooks allow your extension to integrate with Open WebUI at specific points in the application's lifecycle. You can register hook handlers using the `@hook` decorator:

```python
from extension_framework import hook

@hook("ui_init")
def on_ui_init(self) -> None:
    """Hook called when the UI is initialized."""
    logging.info("UI initialized")

@hook("model_before_generate", priority=5)
def on_model_before_generate(self, prompt: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Hook called before generating text."""
    logging.info(f"Generating text with prompt: {prompt[:50]}...")
    # You can modify the prompt or parameters here
    return params
```

The `priority` parameter determines the order in which hook handlers are called. Lower values are called first.

## Creating UI Components

If you're creating a UI extension, you'll need to implement UI components. You can use the `@ui_component` decorator to define components:

```python
from extension_framework import ui_component

@ui_component("my_component", mount_points=["sidebar"])
def render_my_component(extension) -> Dict[str, Any]:
    """Render my component."""
    return {
        "html": """
        <div class="my-component">
            <h2>My Component</h2>
            <p>This is my awesome component!</p>
        </div>
        """
    }
```

You'll also need to define the `components` property and `mount_points` property in your extension class:

```python
@property
def components(self) -> Dict[str, Any]:
    from .ui import get_components
    return get_components()

@property
def mount_points(self) -> Dict[str, List[str]]:
    return {
        "sidebar": ["my_component"],
        "chat": ["another_component"],
    }
```

Available mount points include:

- `sidebar`: The sidebar menu
- `header`: The top header bar
- `footer`: The bottom footer bar
- `chat`: The chat interface
- `settings`: The settings page

## Adding API Endpoints

If you're creating an API extension, you'll need to implement API endpoints. You can use the `@api_route` decorator to define endpoints:

```python
from extension_framework import api_route
from fastapi import HTTPException

@api_route("/my-endpoint", methods=["GET"], summary="My endpoint")
async def my_endpoint(extension) -> Dict[str, Any]:
    """My endpoint."""
    return {
        "extension": extension.name,
        "version": extension.version,
        "message": "Hello from my endpoint!",
    }
```

## Configuring Settings

You can define settings for your extension using the `@setting` decorator:

```python
from extension_framework import setting

@setting(name="greeting_text", default="Hello!", description="Text to display in the greeting")
@setting(name="greeting_color", default="#007bff", description="Color of the greeting text")
@setting(name="show_greeting", default=True, type_=bool, description="Whether to show the greeting")
class MyExtension(Extension):
    # ...
```

These settings will be available in the extension manager UI and can be configured by users.

## Packaging Extensions

Extensions should be packaged as ZIP files for distribution. The ZIP file should contain the extension package directory with the following structure:

```
my-extension/
├── __init__.py
├── ui.py
├── api.py
└── static/
    ├── styles.css
    └── scripts.js
```

## Example Extension

Here's a complete example of a simple extension:

```python
"""
Example Extension for Open WebUI.
"""

import logging
from typing import Dict, List, Any

from extension_framework import (
    UIExtension,
    hook,
    ui_component,
    setting,
)

logger = logging.getLogger("example_extension")

@setting(name="greeting_text", default="Hello from Example Extension!", description="Text to display in the greeting")
@setting(name="greeting_color", default="#007bff", description="Color of the greeting text")
class ExampleExtension(UIExtension):
    """A simple example extension."""
    
    @property
    def name(self) -> str:
        return "example-extension"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    @property
    def description(self) -> str:
        return "A simple example extension to demonstrate how to build extensions."
    
    @property
    def author(self) -> str:
        return "Open WebUI Team"
    
    @property
    def components(self) -> Dict[str, Any]:
        from .ui import get_components
        return get_components()
    
    @property
    def mount_points(self) -> Dict[str, List[str]]:
        return {
            "sidebar": ["example_greeting"],
        }
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the extension."""
        logger.info("Initializing example extension")
        return True
    
    def activate(self) -> bool:
        """Activate the extension."""
        logger.info("Activating example extension")
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension."""
        logger.info("Deactivating example extension")
        return True
    
    @hook("ui_init")
    def on_ui_init(self) -> None:
        """Hook called when the UI is initialized."""
        logger.info("UI initialized")

# Create an instance of the extension
extension = ExampleExtension()
```

For more detailed examples, see the `example_extension` directory in the extension system repository.

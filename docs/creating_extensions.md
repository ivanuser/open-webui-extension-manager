# Creating Extensions for Open WebUI

This guide explains how to create extensions for Open WebUI using the Extension Framework.

## Extension Types

The Extension Framework supports several types of extensions:

- **UI Extensions**: Add new UI components to Open WebUI
- **API Extensions**: Add new API endpoints
- **Model Adapters**: Integrate new AI models
- **Tool Extensions**: Add new tools or capabilities to the system
- **Theme Extensions**: Customize the appearance of Open WebUI

## Basic Structure

A typical extension has the following structure:

```
my_extension/
├── __init__.py           # Main extension entry point
├── api.py                # API endpoints
├── static/               # Static assets
│   └── my_extension.js   # Frontend JavaScript
├── config/               # Configuration files
└── metadata.json         # Extension metadata (optional)
```

## Creating a Simple Extension

### 1. Create the Extension Directory

Create a new directory for your extension:

```bash
mkdir my_extension
cd my_extension
```

### 2. Create the Main Extension File

Create `__init__.py` with the following content:

```python
"""
My Extension for Open WebUI

id: my_extension
name: My Extension
description: A custom extension for Open WebUI
version: 0.1.0
author: Your Name
"""

import os
from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

# Create router
router = APIRouter(prefix="/api/ext/my_extension", tags=["my_extension"])

# Add API routes
@router.get("/hello")
async def hello():
    return {"message": "Hello from My Extension!"}

def get_router():
    """Get the extension's API router."""
    return router

def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    # Register static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount(
            "/extensions/my_extension/static",
            StaticFiles(directory=static_dir),
            name="my_extension_static"
        )
```

### 3. Add Frontend JavaScript

Create a `static` directory and add a JavaScript file:

```bash
mkdir static
touch static/my_extension.js
```

Add the following content to `static/my_extension.js`:

```javascript
// My Extension JavaScript

console.log("My Extension loaded");

// Add UI components when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing My Extension UI");
    
    // Add a menu item to the sidebar
    const addMenuItem = () => {
        const sidebar = document.querySelector('.sidebar-menu');
        if (sidebar && !document.querySelector('.my-extension-menu-item')) {
            const menuItem = document.createElement('div');
            menuItem.className = 'sidebar-menu-item my-extension-menu-item';
            menuItem.innerHTML = `
                <span class="sidebar-menu-item-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </span>
                <span class="sidebar-menu-item-text">My Extension</span>
            `;
            
            sidebar.appendChild(menuItem);
        }
    };
    
    // Try to add the menu item now and retry after a delay
    addMenuItem();
    setTimeout(addMenuItem, 1000);
});
```

## Using the Extension Framework

For more advanced extensions, you can use the Extension Framework classes:

```python
from open_webui.extensions.framework import (
    UIExtension,
    ExtensionContext,
    admin_page,
    sidebar_item
)

@admin_page(title="My Extension", icon="puzzle-piece", path="/admin/myext")
@sidebar_item(title="My Feature", icon="star", path="/myfeature")
class MyExtension(UIExtension):
    """My custom extension."""
    
    id = "my_extension"
    name = "My Extension"
    description = "A custom extension for Open WebUI"
    version = "0.1.0"
    author = "Your Name"
    
    def __init__(self, context: ExtensionContext):
        """Initialize the extension."""
        super().__init__(context)
        
        # Add API routes
        self.router.add_api_route(
            path="/hello",
            endpoint=self.hello,
            methods=["GET"],
            summary="Hello endpoint",
            description="A simple hello endpoint"
        )
    
    async def hello(self):
        """Hello endpoint."""
        return {"message": "Hello from My Extension!"}
```

## Extension Lifecycle

Extensions have the following lifecycle events:

- **Initialization**: When the extension is loaded
- **Startup**: When the extension is started
- **Shutdown**: When the extension is shut down

You can define functions for these events in your extension:

```python
def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    # Initialize resources
    
def on_shutdown(app: FastAPI):
    """Called when the extension shuts down."""
    # Clean up resources
```

## Testing Your Extension

To test your extension:

1. Place your extension in the `extensions` directory of Open WebUI
2. Restart Open WebUI
3. Check the logs for any errors
4. Verify that your extension appears in the Extensions section of the admin panel

## Packaging Your Extension

To package your extension for distribution:

1. Create a ZIP file of your extension directory
2. Share the ZIP file with others
3. Users can install your extension through the Extension Manager

## Next Steps

- Check out the [Extension API Reference](extension_api.md) for more details
- Look at the example extensions in the repository for inspiration
- Join the Open WebUI community to share your extensions

# Open WebUI Extension System

The Open WebUI Extension System provides a comprehensive framework for creating, installing, and managing extensions for Open WebUI. This system allows developers to enhance Open WebUI with new features, integrations, and capabilities.

## Key Features

- **Extension Manager**: User-friendly interface for installing, configuring, and managing extensions
- **Extension Framework**: Standardized framework for creating different types of extensions
- **Integrated API**: Seamless integration with Open WebUI's core features
- **MCP Connector**: Example extension for connecting to Model Context Protocol (MCP) servers

## Installation

### Quick Install (Recommended)

```bash
# Install the Extension Manager directly from GitHub
curl -sSL https://raw.githubusercontent.com/open-webui/extensions/main/install.sh | bash
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/open-webui/extensions.git
   cd extensions
   ```

2. Run the installation script:
   ```bash
   python install.py
   ```

3. Restart Open WebUI to apply changes

### Pip Installation (Coming Soon)

```bash
pip install open-webui-extensions
```

## Using the Extension Manager

After installation, restart Open WebUI and access the Extension Manager:

1. Log in to Open WebUI
2. Go to Admin > Extensions
3. Use the interface to:
   - View installed extensions
   - Install new extensions
   - Enable/disable extensions
   - Configure extension settings
   - Uninstall extensions

## MCP Connector Extension

Included as an example is the MCP Connector extension, which allows connecting to MCP (Model Context Protocol) servers from Open WebUI.

### Features

- Add and manage multiple MCP servers
- Test server connections
- View available models from MCP servers
- Automatically register models for use in Open WebUI

### Usage

1. Navigate to MCP Servers in the sidebar or Admin > MCP Servers
2. Click "Add Server" to add a new MCP server
3. Enter the server details:
   - Name: A friendly name for the server
   - URL: The base URL of the MCP server (e.g., http://localhost:11434/v1)
   - API Key: Optional API key for authentication
   - Description: Optional description of the server
4. Click "Save" to add the server
5. Enable the server to make its models available in Open WebUI

## Creating Extensions

The Extension System provides a standardized framework for creating extensions. Here's a basic guide to get started:

### Extension Types

- **UI Extensions**: Add new UI components to Open WebUI
- **API Extensions**: Add new API endpoints
- **Model Adapters**: Integrate new AI models
- **Tool Extensions**: Add new tools or capabilities to the system
- **Theme Extensions**: Customize the appearance of Open WebUI

### Basic Structure

```
my_extension/
├── __init__.py           # Main extension entry point
├── api.py                # API endpoints
├── static/               # Static assets
│   └── my_extension.js   # Frontend JavaScript
├── config/               # Configuration files
└── metadata.json         # Extension metadata (optional)
```

### Example Extension

```python
"""
Example Extension for Open WebUI

id: example_extension
name: Example Extension
description: An example extension for Open WebUI
version: 0.1.0
author: Your Name
"""

import os
from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

# Create router
router = APIRouter(prefix="/api/ext/example", tags=["example"])

# Add API routes
@router.get("/hello")
async def hello():
    return {"message": "Hello from Example Extension!"}

def get_router():
    """Get the extension's API router."""
    return router

def on_startup(app: FastAPI):
    """Called when the extension starts up."""
    # Register static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount(
            "/extensions/example/static",
            StaticFiles(directory=static_dir),
            name="example_static"
        )
```

## Advanced Extension Development

For more advanced extension development, you can use the Extension Framework classes:

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

## Documentation

For more detailed documentation, see:

- [Extension Manager Guide](docs/extension_manager.md)
- [Creating Extensions](docs/creating_extensions.md)
- [Extension API Reference](docs/extension_api.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

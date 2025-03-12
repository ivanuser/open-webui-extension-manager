# Creating Extensions for Open WebUI

This guide will help you create your own extensions for Open WebUI.

## Extension Types

Open WebUI supports several types of extensions:

1. **UI Extensions**: Add new UI components to Open WebUI
2. **API Extensions**: Add new API endpoints
3. **Model Adapters**: Integrate new AI models
4. **Tool Extensions**: Add new tools or capabilities to the system
5. **Theme Extensions**: Customize the appearance of Open WebUI

## Creating a Simple Extension

Let's create a simple UI extension:

1. Create a new directory for your extension
2. Create an `__init__.py` file with your extension class
3. Implement the required methods

### Example: Hello World Extension

```python
from open_webui_extensions.extension_system.base import UIExtension
from open_webui_extensions.extension_system.decorators import startup_hook, ui_component

class HelloWorldExtension(UIExtension):
    """A simple 'Hello World' extension."""
    
    # Extension metadata
    id = "hello_world"
    name = "Hello World"
    description = "A simple example extension that adds a greeting to the UI."
    version = "1.0.0"
    author = "Your Name"
    
    @startup_hook
    async def on_startup(self):
        """Called when the extension is started."""
        print("Hello World extension started!")
    
    @ui_component(location="settings")
    def hello_world_component(self):
        """Add a greeting to the settings panel."""
        return {
            "type": "div",
            "props": {
                "className": "p-4 bg-gray-100 rounded-md my-4",
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "className": "text-xl font-bold",
                            "children": "Hello from the Extension!"
                        }
                    },
                    {
                        "type": "p",
                        "props": {
                            "className": "mt-2",
                            "children": "This is a simple example component added by the Hello World extension."
                        }
                    }
                ]
            }
        }


Extension Hooks
Extensions can hook into various parts of Open WebUI:

on_startup: Called when the extension is started
on_shutdown: Called when the extension is stopped
on_chat_request: Called before a chat request is processed
on_chat_response: Called after a chat response is generated
on_ui_tab: Called to add a UI component
on_api_route: Called to add an API endpoint
on_tool: Called to add a tool

Packaging Extensions
To package your extension for distribution:

Create a ZIP file containing your extension directory
Upload the ZIP file to the Extension Manager

Installing Extensions
Extensions can be installed via:

The Extension Manager UI
The openwebui-ext CLI tool

Create `docs/extension_api.md`:

```markdown
# Open WebUI Extension API

This document describes the API for Open WebUI extensions.

## Base Extension Class

All extensions must inherit from the `Extension` base class:

```python
from open_webui_extensions.extension_system.base import Extension

class MyExtension(Extension):
    """My custom extension."""
    
    # Extension metadata
    id = "my_extension"
    name = "My Extension"
    description = "A custom extension for Open WebUI."
    version = "1.0.0"
    author = "Your Name"
    
    async def on_startup(self):
        """Called when the extension is started."""
        pass
    
    async def on_shutdown(self):
        """Called when the extension is stopped."""
        pass
    
    def get_settings(self):
        """Get extension settings."""
        return {}
    
    def update_settings(self, settings):
        """Update extension settings."""
        pass

UI Extensions
UI Extensions add new UI components to Open WebUI:
from open_webui_extensions.extension_system.base import UIExtension
from open_webui_extensions.extension_system.decorators import ui_component

class MyUIExtension(UIExtension):
    """My UI extension."""
    
    @ui_component(location="settings", order=0)
    def my_component(self):
        """Add a component to the settings panel."""
        return {
            "type": "div",
            "props": {
                "children": "Hello from my extension!"
            }
        }

API Extensions
API Extensions add new API endpoints to Open WebUI:
from open_webui_extensions.extension_system.base import APIExtension
from open_webui_extensions.extension_system.decorators import api_route

class MyAPIExtension(APIExtension):
    """My API extension."""
    
    @api_route("/hello", methods=["GET"])
    async def hello_endpoint(self):
        """A simple API endpoint."""
        return {"message": "Hello from my extension!"}

Tool Extensions
Tool Extensions add new tools to Open WebUI:
from open_webui_extensions.extension_system.base import ToolExtension
from open_webui_extensions.extension_system.decorators import tool

class MyToolExtension(ToolExtension):
    """My tool extension."""
    
    @tool(name="my_tool", description="A custom tool")
    def my_tool(self, param1, param2):
        """A custom tool."""
        return f"Processed {param1} and {param2}"

Model Adapter Extensions
Model Adapter Extensions add new AI models to Open WebUI:
from open_webui_extensions.extension_system.base import ModelAdapterExtension

class MyModelExtension(ModelAdapterExtension):
    """My model adapter extension."""
    
    async def generate_completion(self, prompt, **kwargs):
        """Generate a completion using the model."""
        # Integrate with your model here
        return "Generated text from my model."

Theme Extensions
Theme Extensions customize the appearance of Open WebUI:
from open_webui_extensions.extension_system.base import ThemeExtension

class MyThemeExtension(ThemeExtension):
    """My theme extension."""
    
    # Path to CSS file
    css_path = "static/theme.css"
    
    # Path to JS file (optional)
    js_path = "static/theme.js"

Hooks
Extensions can use hooks to integrate with Open WebUI:
from open_webui_extensions.extension_system.decorators import startup_hook, shutdown_hook, chat_request_hook, chat_response_hook

@startup_hook
async def on_startup():
    """Called when the extension is started."""
    pass

@shutdown_hook
async def on_shutdown():
    """Called when the extension is stopped."""
    pass

@chat_request_hook
async def on_chat_request(request):
    """Called before a chat request is processed."""
    # Modify request if needed
    return request

@chat_response_hook
async def on_chat_response(response):
    """Called after a chat response is generated."""
    # Modify response if needed
    return response


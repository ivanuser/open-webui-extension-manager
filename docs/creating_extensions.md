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

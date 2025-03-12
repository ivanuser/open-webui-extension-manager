from open_webui_extensions.extension_system.base import UIExtension
from open_webui_extensions.extension_system.decorators import startup_hook, ui_component, api_route

class HelloWorldExtension(UIExtension):
    """A simple 'Hello World' extension."""
    
    # Extension metadata
    id = "hello_world"
    name = "Hello World"
    description = "A simple example extension that adds a greeting to the UI."
    version = "1.0.0"
    author = "Open WebUI Team"
    
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
    
    @api_route("/hello", methods=["GET"])
    async def hello_endpoint(self):
        """A simple API endpoint that returns a greeting."""
        return {"message": "Hello from the Hello World extension!"}

from open_webui_extensions.extension_system.base import ToolExtension
from open_webui_extensions.extension_system.decorators import tool, startup_hook
import random

class WeatherToolExtension(ToolExtension):
    """An example tool extension that provides weather information."""
    
    # Extension metadata
    id = "weather_tool"
    name = "Weather Tool"
    description = "A tool for getting weather information."
    version = "1.0.0"
    author = "Open WebUI Team"
    
    # Weather data (simulated)
    weather_data = {
        "New York": {"temperature": 72, "condition": "Sunny"},
        "London": {"temperature": 65, "condition": "Cloudy"},
        "Tokyo": {"temperature": 78, "condition": "Partly Cloudy"},
        "Sydney": {"temperature": 80, "condition": "Clear"},
        "Paris": {"temperature": 70, "condition": "Rainy"},
    }
    
    @startup_hook
    async def on_startup(self):
        """Called when the extension is started."""
        print("Weather Tool extension started!")
        
        # Register the weather tool
        self.register_tool(
            name="get_weather",
            description="Get the current weather for a location",
            function=self.get_weather
        )
    
    @tool(name="get_weather", description="Get the current weather for a location")
    def get_weather(self, location: str):
        """Get the current weather for a location."""
        # If the location exists in our data, return it
        if location in self.weather_data:
            return self.weather_data[location]
        
        # Otherwise, generate some random weather
        return {
            "temperature": random.randint(60, 85),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy"])
        }

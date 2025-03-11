"""
API endpoints for the example extension.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from extension_framework import api_route

# Create API router
router = APIRouter(prefix="/api/example", tags=["example"])

@api_route("/greeting", methods=["GET"], summary="Get the example greeting")
async def get_greeting(extension) -> Dict[str, Any]:
    """Get the example greeting."""
    return {
        "greeting": extension.greeting_text,
        "color": extension.greeting_color,
        "show": extension.show_greeting,
    }

@api_route("/echo", methods=["POST"], summary="Echo back the request body")
async def echo(extension, body: Dict[str, Any]) -> Dict[str, Any]:
    """Echo back the request body."""
    return {
        "extension": extension.name,
        "version": extension.version,
        "echo": body,
    }

@api_route("/weather/{location}", methods=["GET"], summary="Get mock weather for a location")
async def get_weather(extension, location: str) -> Dict[str, Any]:
    """Get mock weather for a location."""
    # This is just a mock API for demonstration purposes
    weather_data = {
        "new york": {
            "temperature": 72,
            "conditions": "Sunny",
            "humidity": 45,
        },
        "london": {
            "temperature": 62,
            "conditions": "Cloudy",
            "humidity": 80,
        },
        "tokyo": {
            "temperature": 85,
            "conditions": "Partly Cloudy",
            "humidity": 60,
        },
    }
    
    location_lower = location.lower()
    if location_lower in weather_data:
        return {
            "location": location,
            "weather": weather_data[location_lower],
            "powered_by": f"{extension.name} v{extension.version}",
        }
    else:
        raise HTTPException(status_code=404, detail=f"Weather data not found for {location}")

def get_router() -> APIRouter:
    """Get the API router for the extension."""
    return router

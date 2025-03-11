"""
API endpoints for the MCP Connector extension.
"""

import logging
from typing import Dict, List, Any, Optional, Union
from fastapi import APIRouter, HTTPException

from .mcp_client import MCPServerManager, MCPServerConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_connector.api")

# Initialize server manager
server_manager = MCPServerManager()

def setup_routes(router: APIRouter):
    """Set up API routes for the MCP Connector."""
    
    @router.get("/servers")
    async def get_servers():
        """Get all registered MCP servers."""
        servers = server_manager.load_servers()
        
        # Add status information
        server_responses = []
        for server in servers:
            status = "Unknown"
            try:
                if await server_manager.test_connection(server.name):
                    status = "Connected"
                else:
                    status = "Disconnected"
            except Exception as e:
                status = f"Error: {str(e)}"
            
            server_responses.append({
                "name": server.name,
                "url": server.url,
                "description": server.description,
                "enabled": server.enabled,
                "status": status
            })
        
        return server_responses
    
    @router.post("/servers")
    async def create_server(server: dict):
        """Create a new MCP server."""
        server_config = MCPServerConfig(**server)
        
        if not server_manager.add_server(server_config):
            raise HTTPException(
                status_code=400,
                detail=f"Server with name '{server_config.name}' already exists"
            )
        
        status = "Unknown"
        try:
            if await server_manager.test_connection(server_config.name):
                status = "Connected"
            else:
                status = "Disconnected"
        except Exception as e:
            status = f"Error: {str(e)}"
        
        return {
            "name": server_config.name,
            "url": server_config.url,
            "description": server_config.description,
            "enabled": server_config.enabled,
            "status": status
        }
    
    @router.put("/servers/{server_name}")
    async def update_server(server_name: str, server: dict):
        """Update an existing MCP server."""
        server_config = MCPServerConfig(**server)
        
        if not server_manager.update_server(server_name, server_config):
            raise HTTPException(
                status_code=404,
                detail=f"Server '{server_name}' not found"
            )
        
        status = "Unknown"
        try:
            if await server_manager.test_connection(server_config.name):
                status = "Connected"
            else:
                status = "Disconnected"
        except Exception as e:
            status = f"Error: {str(e)}"
        
        return {
            "name": server_config.name,
            "url": server_config.url,
            "description": server_config.description,
            "enabled": server_config.enabled,
            "status": status
        }
    
    @router.delete("/servers/{server_name}")
    async def delete_server(server_name: str):
        """Delete an MCP server."""
        if not server_manager.remove_server(server_name):
            raise HTTPException(
                status_code=404,
                detail=f"Server '{server_name}' not found"
            )
        
        return {"message": f"Server '{server_name}' deleted successfully"}
    
    @router.post("/servers/{server_name}/toggle")
    async def toggle_server(server_name: str, toggle: dict):
        """Enable or disable an MCP server."""
        enable = toggle.get("enable")
        
        server = server_manager.get_server(server_name)
        if not server:
            raise HTTPException(
                status_code=404,
                detail=f"Server '{server_name}' not found"
            )
        
        # Determine the new enabled state
        if enable is None:
            enable = not server.enabled
        
        # Update the server
        server.enabled = enable
        if not server_manager.update_server(server_name, server):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update server '{server_name}'"
            )
        
        status = "Unknown"
        try:
            if enable and await server_manager.test_connection(server_name):
                status = "Connected"
            elif enable:
                status = "Disconnected"
            else:
                status = "Disabled"
        except Exception as e:
            status = f"Error: {str(e)}"
        
        return {
            "name": server.name,
            "url": server.url,
            "description": server.description,
            "enabled": server.enabled,
            "status": status
        }
    
    @router.get("/servers/{server_name}/test")
    async def test_server(server_name: str):
        """Test connection to an MCP server."""
        server = server_manager.get_server(server_name)
        if not server:
            raise HTTPException(
                status_code=404,
                detail=f"Server '{server_name}' not found"
            )
        
        try:
            connected = await server_manager.test_connection(server_name)
            
            if connected:
                return {
                    "status": "Connected",
                    "message": "Successfully connected to MCP server"
                }
            else:
                return {
                    "status": "Disconnected",
                    "message": "Could not connect to MCP server"
                }
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Error connecting to MCP server: {str(e)}"
            }
    
    @router.get("/servers/{server_name}/models")
    async def get_server_models(server_name: str):
        """Get models from a specific MCP server."""
        server = server_manager.get_server(server_name)
        if not server:
            raise HTTPException(
                status_code=404,
                detail=f"Server '{server_name}' not found"
            )
        
        if not server.enabled:
            raise HTTPException(
                status_code=400,
                detail=f"Server '{server_name}' is disabled"
            )
        
        try:
            models = await server_manager.get_server_models(server_name)
            
            return [
                {
                    "id": model.get("id", "unknown"),
                    "name": model.get("name", model.get("id", "unknown")),
                    "server": server_name
                }
                for model in models
            ]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error listing models: {str(e)}"
            )
    
    @router.get("/models")
    async def get_all_models():
        """Get models from all MCP servers."""
        all_models = await server_manager.get_all_models()
        
        model_responses = []
        for server_name, models in all_models.items():
            for model in models:
                model_responses.append({
                    "id": model.get("id", "unknown"),
                    "name": model.get("name", model.get("id", "unknown")),
                    "server": server_name
                })
        
        return model_responses

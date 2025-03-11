"""
MCP Client module for interacting with MCP (Model Context Protocol) servers.
"""

import os
import json
import logging
import aiohttp
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_connector.client")

class MCPServerConfig(BaseModel):
    """Configuration for an MCP server."""
    name: str
    url: str
    api_key: str = ""
    description: str = ""
    enabled: bool = True

class MCPClient:
    """Client for interacting with MCP servers."""
    
    def __init__(self, server_url: str, api_key: str = "", timeout: int = 30):
        """Initialize the MCP client."""
        self.server_url = server_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
    
    async def test_connection(self) -> bool:
        """Test connection to the MCP server."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/models",
                    headers=headers,
                    timeout=5
                ) as response:
                    return response.status == 200
        except Exception:
            return False
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List models from the MCP server."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.server_url}/models",
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status != 200:
                        return []
                    
                    data = await response.json()
                    return data.get("data", [])
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []

class MCPServerManager:
    """Manager for MCP server configurations."""
    
    def __init__(self):
        """Initialize the MCP server manager."""
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "servers.json")
        self.servers: Dict[str, MCPServerConfig] = {}
        
        # Create the config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load server configurations
        self.load_servers()
    
    def _get_config_dir(self) -> str:
        """Get the directory for configuration files."""
        # Get the extension directory
        extension_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(extension_dir, "config")
    
    def load_servers(self) -> List[MCPServerConfig]:
        """Load server configurations from the config file."""
        if not os.path.exists(self.config_file):
            # Create a default config with an example server
            self.servers = {
                "example": MCPServerConfig(
                    name="Example MCP Server",
                    url="http://localhost:11434/v1",
                    api_key="",
                    description="Example MCP server. Replace with your own server.",
                    enabled=False
                )
            }
            self._save_servers()
        
        try:
            with open(self.config_file, "r") as f:
                servers_data = json.load(f)
                
                self.servers = {}
                for key, data in servers_data.items():
                    self.servers[key] = MCPServerConfig(**data)
        except Exception as e:
            logger.error(f"Error loading server configurations: {str(e)}")
            
            # Create default config if loading fails
            if not self.servers:
                self.servers = {
                    "example": MCPServerConfig(
                        name="Example MCP Server",
                        url="http://localhost:11434/v1",
                        api_key="",
                        description="Example MCP server. Replace with your own server.",
                        enabled=False
                    )
                }
                self._save_servers()
        
        return list(self.servers.values())
    
    def _save_servers(self) -> bool:
        """Save server configurations to the config file."""
        try:
            servers_data = {}
            for key, server in self.servers.items():
                servers_data[key] = server.dict()
            
            with open(self.config_file, "w") as f:
                json.dump(servers_data, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Error saving server configurations: {str(e)}")
            return False
    
    def get_server(self, server_name: str) -> Optional[MCPServerConfig]:
        """Get a server configuration by name."""
        for key, server in self.servers.items():
            if server.name == server_name:
                return server
        return None
    
    def add_server(self, server: MCPServerConfig) -> bool:
        """Add a new server configuration."""
        # Check if server with same name already exists
        if self.get_server(server.name):
            return False
        
        # Generate a key for the server
        key = server.name.replace(" ", "_").lower()
        
        # Add the server
        self.servers[key] = server
        
        # Save the servers
        return self._save_servers()
    
    def update_server(self, server_name: str, server: MCPServerConfig) -> bool:
        """Update an existing server configuration."""
        # Find the server
        old_key = None
        for key, s in self.servers.items():
            if s.name == server_name:
                old_key = key
                break
        
        if old_key is None:
            return False
        
        # If the name changed, generate a new key
        if server.name != server_name:
            # Check if server with new name already exists
            if self.get_server(server.name):
                return False
            
            # Delete the old server
            del self.servers[old_key]
            
            # Generate a new key
            key = server.name.replace(" ", "_").lower()
        else:
            key = old_key
        
        # Update the server
        self.servers[key] = server
        
        # Save the servers
        return self._save_servers()
    
    def remove_server(self, server_name: str) -> bool:
        """Remove a server configuration."""
        # Find the server
        key = None
        for k, server in self.servers.items():
            if server.name == server_name:
                key = k
                break
        
        if key is None:
            return False
        
        # Remove the server
        del self.servers[key]
        
        # Save the servers
        return self._save_servers()
    
    async def test_connection(self, server_name: str) -> bool:
        """Test connection to a server."""
        server = self.get_server(server_name)
        if not server:
            return False
        
        client = MCPClient(server.url, server.api_key)
        return await client.test_connection()
    
    async def get_server_models(self, server_name: str) -> List[Dict[str, Any]]:
        """Get models from a specific server."""
        server = self.get_server(server_name)
        if not server or not server.enabled:
            return []
        
        client = MCPClient(server.url, server.api_key)
        return await client.list_models()
    
    async def get_all_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get models from all enabled servers."""
        results = {}
        
        for server in self.servers.values():
            if not server.enabled:
                continue
            
            models = await self.get_server_models(server.name)
            results[server.name] = models
        
        return results

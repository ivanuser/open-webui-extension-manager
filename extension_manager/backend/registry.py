"""
Extension Registry for Open WebUI.

This module handles the discovery, loading, and management of extensions.
"""

import os
import sys
import json
import logging
import shutil
import importlib
import inspect
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("extension_manager.registry")

class ExtensionRegistry:
    """Registry for managing extensions."""
    
    def __init__(self, root_dir: str):
        """Initialize the extension registry.
        
        Args:
            root_dir: The root directory of Open WebUI
        """
        self.root_dir = root_dir
        self.extensions_dir = os.path.join(root_dir, "extensions")
        self.config_path = os.path.join(root_dir, "config", "extensions.json")
        self._extensions_cache = None
        
        # Create directories if they don't exist
        os.makedirs(self.extensions_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Initialize the config file if it doesn't exist
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                json.dump({"extensions": []}, f, indent=2)
    
    def get_extensions(self) -> List[Dict[str, Any]]:
        """Get all registered extensions."""
        if self._extensions_cache is not None:
            return self._extensions_cache
        
        # Load extensions from config file
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                extensions = []
                
                for ext_data in config.get("extensions", []):
                    ext_id = ext_data.get("id")
                    ext_path = os.path.join(self.extensions_dir, ext_id)
                    
                    # Check if extension directory exists
                    if not os.path.exists(ext_path):
                        logger.warning(f"Extension directory not found: {ext_path}")
                        continue
                    
                    # Load extension metadata
                    metadata = self._load_extension_metadata(ext_path)
                    if metadata:
                        # Combine metadata with config data
                        extension = {
                            "id": ext_id,
                            "name": metadata.get("name", ext_data.get("name", ext_id)),
                            "description": metadata.get("description", ext_data.get("description", "")),
                            "version": metadata.get("version", ext_data.get("version", "0.1.0")),
                            "author": metadata.get("author", ext_data.get("author", "Unknown")),
                            "author_url": metadata.get("author_url", ext_data.get("author_url")),
                            "repository_url": metadata.get("repository_url", ext_data.get("repository_url")),
                            "license": metadata.get("license", ext_data.get("license")),
                            "tags": metadata.get("tags", ext_data.get("tags", [])),
                            "enabled": ext_data.get("enabled", True),
                            "installed_at": ext_data.get("installed_at", "Unknown"),
                            "updated_at": ext_data.get("updated_at", "Unknown"),
                            "path": ext_path,
                            "config": ext_data.get("config", {})
                        }
                        extensions.append(extension)
                
                self._extensions_cache = extensions
                return extensions
        except Exception as e:
            logger.error(f"Error loading extensions: {e}")
            return []
    
    def get_extension_by_id(self, extension_id: str) -> Optional[Dict[str, Any]]:
        """Get an extension by ID."""
        extensions = self.get_extensions()
        for extension in extensions:
            if extension["id"] == extension_id:
                return extension
        return None
    
    def install_extension(self, source_dir: str) -> Dict[str, Any]:
        """Install an extension from a directory.
        
        Args:
            source_dir: The source directory of the extension
            
        Returns:
            The installed extension
            
        Raises:
            Exception: If the extension cannot be installed
        """
        try:
            # Load extension metadata
            metadata = self._load_extension_metadata(source_dir)
            if not metadata:
                raise Exception("Invalid extension: missing metadata")
            
            extension_id = metadata.get("id")
            if not extension_id:
                # Try to derive ID from directory name
                extension_id = os.path.basename(source_dir).lower().replace(" ", "_")
                metadata["id"] = extension_id
            
            # Check if extension already exists
            target_dir = os.path.join(self.extensions_dir, extension_id)
            update_existing = os.path.exists(target_dir)
            
            # Copy extension files
            if update_existing:
                shutil.rmtree(target_dir)
            shutil.copytree(source_dir, target_dir)
            
            # Register the extension
            extension = self._register_extension(extension_id, metadata, update_existing)
            
            # Clear the cache
            self._extensions_cache = None
            
            return extension
        
        except Exception as e:
            logger.error(f"Error installing extension: {e}")
            raise
    
    def toggle_extension(self, extension_id: str, enabled: bool) -> Dict[str, Any]:
        """Enable or disable an extension.
        
        Args:
            extension_id: The ID of the extension
            enabled: Whether to enable or disable the extension
            
        Returns:
            The updated extension
            
        Raises:
            Exception: If the extension cannot be toggled
        """
        try:
            # Get the extension
            extension = self.get_extension_by_id(extension_id)
            if not extension:
                raise Exception(f"Extension '{extension_id}' not found")
            
            # Update the config
            with open(self.config_path, "r") as f:
                config = json.load(f)
            
            for ext in config.get("extensions", []):
                if ext.get("id") == extension_id:
                    ext["enabled"] = enabled
                    break
            
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            # Clear the cache
            self._extensions_cache = None
            
            # Get the updated extension
            return self.get_extension_by_id(extension_id)
        
        except Exception as e:
            logger.error(f"Error toggling extension: {e}")
            raise
    
    def delete_extension(self, extension_id: str) -> bool:
        """Delete an extension.
        
        Args:
            extension_id: The ID of the extension
            
        Returns:
            True if the extension was deleted successfully, False otherwise
        """
        try:
            # Get the extension
            extension = self.get_extension_by_id(extension_id)
            if not extension:
                return False
            
            # Remove the extension directory
            ext_path = os.path.join(self.extensions_dir, extension_id)
            if os.path.exists(ext_path):
                shutil.rmtree(ext_path)
            
            # Update the config
            with open(self.config_path, "r") as f:
                config = json.load(f)
            
            config["extensions"] = [ext for ext in config.get("extensions", []) 
                                   if ext.get("id") != extension_id]
            
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            # Clear the cache
            self._extensions_cache = None
            
            return True
        
        except Exception as e:
            logger.error(f"Error deleting extension: {e}")
            return False
    
    def _load_extension_metadata(self, extension_dir: str) -> Dict[str, Any]:
        """Load extension metadata from an extension directory."""
        try:
            # Check for metadata.json
            metadata_file = os.path.join(extension_dir, "metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    return json.load(f)
            
            # Check for metadata in __init__.py
            init_file = os.path.join(extension_dir, "__init__.py")
            if os.path.exists(init_file):
                with open(init_file, "r") as f:
                    content = f.read()
                
                metadata = {}
                
                # Extract metadata from docstring
                import re
                docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
                if docstring_match:
                    docstring = docstring_match.group(1)
                    
                    # Parse key-value pairs from docstring
                    for line in docstring.split("\n"):
                        line = line.strip()
                        if ": " in line:
                            key, value = line.split(": ", 1)
                            metadata[key.lower()] = value
                
                # Extract metadata from module variables
                for var_name in ["__id__", "__name__", "__description__", "__version__", "__author__", 
                               "__author_url__", "__repository_url__", "__license__", "__tags__"]:
                    match = re.search(fr'{var_name}\s*=\s*[\'"](.+?)[\'"]', content)
                    if match:
                        key = var_name.strip("_").lower()
                        metadata[key] = match.group(1)
                    elif var_name == "__tags__":
                        # Try to find tags as a list
                        match = re.search(fr'{var_name}\s*=\s*\[(.*?)\]', content)
                        if match:
                            tags_str = match.group(1)
                            # Parse the tags list
                            tags = []
                            for tag in tags_str.split(","):
                                tag = tag.strip().strip('"\'')
                                if tag:
                                    tags.append(tag)
                            metadata["tags"] = tags
                
                return metadata
            
            return {}
        
        except Exception as e:
            logger.error(f"Error loading extension metadata: {e}")
            return {}
    
    def _register_extension(self, extension_id: str, metadata: Dict[str, Any], 
                           update_existing: bool = False) -> Dict[str, Any]:
        """Register an extension in the configuration file.
        
        Args:
            extension_id: The ID of the extension
            metadata: The extension metadata
            update_existing: Whether to update an existing extension
            
        Returns:
            The registered extension
        """
        try:
            # Get the current config
            with open(self.config_path, "r") as f:
                config = json.load(f)
            
            # Check if extension is already registered
            existing_index = None
            for i, ext in enumerate(config.get("extensions", [])):
                if ext.get("id") == extension_id:
                    existing_index = i
                    break
            
            # Prepare extension data
            now = datetime.now().isoformat()
            
            extension_data = {
                "id": extension_id,
                "name": metadata.get("name", extension_id),
                "description": metadata.get("description", ""),
                "version": metadata.get("version", "0.1.0"),
                "author": metadata.get("author", "Unknown"),
                "enabled": True,
                "updated_at": now
            }
            
            # Add optional metadata
            for key in ["author_url", "repository_url", "license", "tags"]:
                if key in metadata:
                    extension_data[key] = metadata[key]
            
            # Update or add the extension
            if existing_index is not None:
                # Preserve the installed_at date and enabled state
                extension_data["installed_at"] = config["extensions"][existing_index].get("installed_at", now)
                extension_data["enabled"] = config["extensions"][existing_index].get("enabled", True)
                config["extensions"][existing_index] = extension_data
            else:
                extension_data["installed_at"] = now
                if "extensions" not in config:
                    config["extensions"] = []
                config["extensions"].append(extension_data)
            
            # Save the updated config
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
            
            # Add path to extension data
            extension_data["path"] = os.path.join(self.extensions_dir, extension_id)
            
            return extension_data
        
        except Exception as e:
            logger.error(f"Error registering extension: {e}")
            raise

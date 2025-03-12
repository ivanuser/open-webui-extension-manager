from typing import Dict, List, Optional, Any, Type
import importlib
import importlib.util
import inspect
import os
import sys
import json
import shutil
import logging
import pkg_resources
from pathlib import Path

from .base import Extension

logger = logging.getLogger("open_webui_extensions")

class ExtensionRegistry:
    """Registry for discovering and loading extensions."""
    
    _instance = None
    extensions: Dict[str, Extension] = {}
    extension_dirs: List[str] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExtensionRegistry, cls).__new__(cls)
            cls._instance.extensions = {}
            
            # Set up extension directories
            home_dir = os.path.expanduser("~")
            cls._instance.extension_dirs = [
                os.path.join(home_dir, ".openwebui", "extensions"),
                # Add more potential extension directories here
            ]
            
            # Ensure extension directories exist
            for ext_dir in cls._instance.extension_dirs:
                os.makedirs(ext_dir, exist_ok=True)
        
        return cls._instance
    
    def discover_extensions(self) -> List[str]:
        """Discover all available extensions."""
        extension_ids = []
        
        # Check each extension directory
        for ext_dir in self.extension_dirs:
            if not os.path.exists(ext_dir):
                continue
            
            # Look for extension packages
            for item in os.listdir(ext_dir):
                item_path = os.path.join(ext_dir, item)
                
                # Skip non-directories
                if not os.path.isdir(item_path):
                    continue
                
                # Check if it's a Python package
                init_file = os.path.join(item_path, "__init__.py")
                if os.path.exists(init_file):
                    extension_ids.append(item)
        
        # Also discover installed extensions via entry points
        for entry_point in pkg_resources.iter_entry_points('open_webui_extensions'):
            extension_ids.append(entry_point.name)
        
        return extension_ids
    
    def load_extension(self, extension_id: str) -> Optional[Extension]:
        """Load an extension by ID."""
        if extension_id in self.extensions:
            return self.extensions[extension_id]
        
        # Check if it's an installed entry point
        for entry_point in pkg_resources.iter_entry_points('open_webui_extensions'):
            if entry_point.name == extension_id:
                try:
                    extension_class = entry_point.load()
                    extension = extension_class()
                    extension.id = extension_id
                    extension.installed = True
                    self.extensions[extension_id] = extension
                    return extension
                except Exception as e:
                    logger.error(f"Error loading extension {extension_id} from entry point: {str(e)}")
                    return None
        
        # Check each extension directory
        for ext_dir in self.extension_dirs:
            ext_path = os.path.join(ext_dir, extension_id)
            if not os.path.exists(ext_path):
                continue
            
            # Add to Python path
            if ext_path not in sys.path:
                sys.path.insert(0, ext_dir)
            
            try:
                # Import the module
                module = importlib.import_module(extension_id)
                
                # Find extension class
                extension_class = None
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Extension) and obj is not Extension:
                        extension_class = obj
                        break
                
                if extension_class:
                    extension = extension_class()
                    extension.id = extension_id
                    extension.installed = True
                    extension.path = ext_path
                    self.extensions[extension_id] = extension
                    return extension
                
            except ImportError as e:
                logger.error(f"Error importing extension {extension_id}: {str(e)}")
            except Exception as e:
                logger.error(f"Error loading extension {extension_id}: {str(e)}")
        
        return None
    
    def get_extension(self, extension_id: str) -> Optional[Extension]:
        """Get an extension by ID."""
        if extension_id in self.extensions:
            return self.extensions[extension_id]
        
        return self.load_extension(extension_id)
    
    def get_all_extensions(self) -> Dict[str, Extension]:
        """Get all loaded extensions."""
        # Discover and load any new extensions
        for extension_id in self.discover_extensions():
            if extension_id not in self.extensions:
                self.load_extension(extension_id)
        
        return self.extensions
    
    def enable_extension(self, extension_id: str) -> bool:
        """Enable an extension."""
        extension = self.get_extension(extension_id)
        if not extension:
            return False
        
        extension.enabled = True
        
        # Save enabled state
        self._save_extension_state(extension_id, True)
        
        return True
    
    def disable_extension(self, extension_id: str) -> bool:
        """Disable an extension."""
        extension = self.get_extension(extension_id)
        if not extension:
            return False
        
        extension.enabled = False
        
        # Save enabled state
        self._save_extension_state(extension_id, False)
        
        return True
    
    def install_extension(self, source_path: str, extension_id: str = None) -> Optional[str]:
        """Install an extension from a directory."""
        # Ensure source path exists
        if not os.path.exists(source_path):
            logger.error(f"Source path does not exist: {source_path}")
            return None
        
        # If no extension_id is provided, use the directory name
        if not extension_id:
            extension_id = os.path.basename(source_path)
        
        # Destination directory
        dest_dir = os.path.join(self.extension_dirs[0], extension_id)
        
        # Remove existing extension if it exists
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        
        # Copy extension files
        shutil.copytree(source_path, dest_dir)
        
        # Load the extension
        extension = self.load_extension(extension_id)
        if extension:
            return extension_id
        
        return None
    
    def uninstall_extension(self, extension_id: str) -> bool:
        """Uninstall an extension."""
        extension = self.get_extension(extension_id)
        if not extension or not extension.path:
            return False
        
        # Disable the extension first
        self.disable_extension(extension_id)
        
        # Remove the extension directory
        if os.path.exists(extension.path):
            shutil.rmtree(extension.path)
        
        # Remove from loaded extensions
        if extension_id in self.extensions:
            del self.extensions[extension_id]
        
        return True
    
    def _save_extension_state(self, extension_id: str, enabled: bool) -> None:
        """Save extension state to a configuration file."""
        config_file = os.path.join(self.extension_dirs[0], "extension_config.json")
        
        # Load existing config
        config = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
            except:
                pass
        
        # Update config
        if "enabled" not in config:
            config["enabled"] = []
        
        if enabled:
            if extension_id not in config["enabled"]:
                config["enabled"].append(extension_id)
        else:
            if extension_id in config["enabled"]:
                config["enabled"].remove(extension_id)
        
        # Save config
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    
    def _load_extension_states(self) -> Dict[str, bool]:
        """Load extension states from configuration file."""
        config_file = os.path.join(self.extension_dirs[0], "extension_config.json")
        
        # Default states
        states = {}
        
        # Load config if it exists
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    
                    # Set states based on enabled list
                    enabled_extensions = config.get("enabled", [])
                    for extension_id in self.discover_extensions():
                        states[extension_id] = extension_id in enabled_extensions
            except:
                pass
        
        return states
    
    def load_all_extensions(self) -> None:
        """Load all discovered extensions and their states."""
        # Discover available extensions
        extension_ids = self.discover_extensions()
        
        # Load extension states
        states = self._load_extension_states()
        
        # Load each extension
        for extension_id in extension_ids:
            extension = self.load_extension(extension_id)
            if extension:
                # Set enabled state
                extension.enabled = states.get(extension_id, False)

# Singleton instance
extension_registry = ExtensionRegistry()

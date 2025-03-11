"""
Extension Registry for Open WebUI.

This module handles the discovery, loading, and management of extensions.
"""

import os
import logging
import json
import yaml
import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
import threading

from extension_framework import (
    Extension,
    load_extension,
    discover_extensions,
    load_extension_config,
    save_extension_config,
    install_extension_from_zip,
    install_extension_from_url,
    install_extension_from_directory,
    uninstall_extension,
    resolve_extension_dependencies,
    sort_extensions_by_dependencies,
)

from .models import (
    ExtensionInfo,
    ExtensionStatus,
    ExtensionType,
    ExtensionSource,
    ExtensionSetting,
    ExtensionDependency,
    ExtensionFilters,
)

logger = logging.getLogger("extension_registry")

class ExtensionRegistry:
    """Registry for managing extensions."""
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ExtensionRegistry, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, extensions_dir: str = None, config_file: str = None):
        """Initialize the extension registry.
        
        Args:
            extensions_dir: The directory containing the extensions.
            config_file: The path to the registry configuration file.
        """
        with self._lock:
            if self._initialized:
                return
            
            self.extensions_dir = extensions_dir or os.environ.get("EXTENSIONS_DIR", "./extensions")
            self.config_file = config_file or os.environ.get("REGISTRY_CONFIG", os.path.join(self.extensions_dir, "registry.yaml"))
            
            # Create extensions directory if it doesn't exist
            os.makedirs(self.extensions_dir, exist_ok=True)
            
            # Initialize internal state
            self.extensions: Dict[str, ExtensionInfo] = {}
            self.instances: Dict[str, Extension] = {}
            
            # Load the registry configuration
            self._load_config()
            
            self._initialized = True
    
    def _load_config(self) -> None:
        """Load the registry configuration."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    if self.config_file.endswith(".yaml") or self.config_file.endswith(".yml"):
                        config = yaml.safe_load(f) or {}
                    elif self.config_file.endswith(".json"):
                        config = json.load(f)
                    else:
                        logger.warning(f"Unknown config file format: {self.config_file}")
                        config = {}
                
                # Load extensions from config
                if "extensions" in config:
                    for ext_info in config["extensions"]:
                        self.extensions[ext_info["name"]] = ExtensionInfo(**ext_info)
        except Exception as e:
            logger.error(f"Error loading registry configuration: {e}")
    
    def _save_config(self) -> None:
        """Save the registry configuration."""
        try:
            config = {
                "extensions": [ext.dict() for ext in self.extensions.values()]
            }
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, "w", encoding="utf-8") as f:
                if self.config_file.endswith(".yaml") or self.config_file.endswith(".yml"):
                    yaml.dump(config, f, default_flow_style=False)
                elif self.config_file.endswith(".json"):
                    json.dump(config, f, indent=2)
                else:
                    logger.warning(f"Unknown config file format: {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving registry configuration: {e}")
    
    def discover(self) -> Dict[str, ExtensionInfo]:
        """Discover installed extensions.
        
        Returns:
            A dictionary mapping extension names to extension information.
        """
        with self._lock:
            # Get paths to potential extension modules
            extension_paths = discover_extensions(self.extensions_dir)
            
            # Load extensions from paths
            loaded_extensions = []
            for path in extension_paths:
                try:
                    extension = load_extension(path)
                    if extension is not None:
                        loaded_extensions.append(extension)
                except Exception as e:
                    logger.error(f"Error loading extension from {path}: {e}")
            
            # Update registry with loaded extensions
            for ext in loaded_extensions:
                ext_info = self._create_extension_info(ext, os.path.dirname(path))
                # Update existing extension or add new one
                self.extensions[ext.name] = ext_info
                self.instances[ext.name] = ext
            
            # Save the updated registry configuration
            self._save_config()
            
            return self.extensions
    
    def _create_extension_info(self, extension: Extension, path: str) -> ExtensionInfo:
        """Create extension information from an extension instance.
        
        Args:
            extension: The extension instance.
            path: The path to the extension.
            
        Returns:
            The extension information.
        """
        # Convert extension type to enum
        ext_type = ExtensionType(extension.type)
        
        # Get extension status from registry or set to inactive
        status = ExtensionStatus.INACTIVE
        if extension.name in self.extensions:
            status = self.extensions[extension.name].status
        
        # Convert dependencies to proper format
        dependencies = []
        for dep in extension.dependencies:
            # Handle simple string dependencies
            if isinstance(dep, str):
                dependencies.append(ExtensionDependency(name=dep))
            # Handle dictionary dependencies with version info
            elif isinstance(dep, dict) and "name" in dep:
                dependencies.append(ExtensionDependency(**dep))
        
        # Convert settings to proper format
        settings = []
        for key, value in extension.settings.items():
            # Handle dictionary settings
            if isinstance(value, dict) and "default" in value:
                settings.append(ExtensionSetting(name=key, **value))
            # Handle simple settings
            else:
                settings.append(ExtensionSetting(
                    name=key,
                    type=type(value).__name__ if value is not None else "str",
                    default=value,
                    value=value,
                    description=f"Setting for {key}"
                ))
        
        # Create extension info
        ext_info = ExtensionInfo(
            name=extension.name,
            version=extension.version,
            description=extension.description,
            author=extension.author,
            type=ext_type,
            status=status,
            source=ExtensionSource.LOCAL,
            path=path,
            dependencies=dependencies,
            settings=settings,
            installed_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        
        return ext_info
    
    def get_extension_info(self, name: str) -> Optional[ExtensionInfo]:
        """Get information about an extension.
        
        Args:
            name: The name of the extension.
            
        Returns:
            The extension information, or None if not found.
        """
        with self._lock:
            return self.extensions.get(name)
    
    def get_extension_instance(self, name: str) -> Optional[Extension]:
        """Get an extension instance.
        
        Args:
            name: The name of the extension.
            
        Returns:
            The extension instance, or None if not found.
        """
        with self._lock:
            return self.instances.get(name)
    
    def list_extensions(self, filters: Optional[ExtensionFilters] = None) -> List[ExtensionInfo]:
        """List all extensions.
        
        Args:
            filters: Filters to apply to the list.
            
        Returns:
            A list of extension information.
        """
        with self._lock:
            # If no extensions in registry, discover them
            if not self.extensions:
                self.discover()
            
            # Filter extensions based on criteria
            extensions = list(self.extensions.values())
            
            if filters:
                # Filter by type
                if filters.types:
                    extensions = [ext for ext in extensions if ext.type in filters.types]
                
                # Filter by status
                if filters.status:
                    extensions = [ext for ext in extensions if ext.status in filters.status]
                
                # Filter by source
                if filters.sources:
                    extensions = [ext for ext in extensions if ext.source in filters.sources]
                
                # Filter by search query
                if filters.search:
                    search = filters.search.lower()
                    extensions = [ext for ext in extensions if (
                        search in ext.name.lower() or
                        search in ext.description.lower() or
                        search in ext.author.lower()
                    )]
            
            return extensions
    
    def install_extension(self, source: ExtensionSource, url: Optional[str] = None, path: Optional[str] = None, name: Optional[str] = None) -> Tuple[bool, Optional[ExtensionInfo], str]:
        """Install an extension.
        
        Args:
            source: The source of the extension.
            url: The URL of the extension (for remote sources).
            path: The path to the extension (for local sources).
            name: The name of the extension (for marketplace sources).
            
        Returns:
            A tuple containing:
            - A boolean indicating success or failure.
            - The extension information if successful, None otherwise.
            - A message describing the result.
        """
        with self._lock:
            try:
                extension_path = None
                
                # Install from different sources
                if source == ExtensionSource.REMOTE and url:
                    extension_path = install_extension_from_url(url, self.extensions_dir)
                elif source == ExtensionSource.LOCAL and path:
                    extension_path = install_extension_from_directory(path, self.extensions_dir)
                elif source == ExtensionSource.MARKETPLACE and name:
                    # TODO: Implement marketplace extension installation
                    return False, None, f"Marketplace installation not implemented yet"
                else:
                    return False, None, f"Invalid extension source or missing parameters"
                
                if not extension_path:
                    return False, None, f"Failed to install extension"
                
                # Load the installed extension
                init_path = os.path.join(extension_path, "__init__.py")
                extension = load_extension(init_path)
                
                if not extension:
                    return False, None, f"Failed to load installed extension"
                
                # Create extension info
                ext_info = self._create_extension_info(extension, extension_path)
                
                # Update registry
                self.extensions[extension.name] = ext_info
                self.instances[extension.name] = extension
                
                # Save registry configuration
                self._save_config()
                
                return True, ext_info, f"Extension {extension.name} installed successfully"
            except Exception as e:
                logger.error(f"Error installing extension: {e}")
                return False, None, f"Error installing extension: {e}"
    
    def uninstall_extension(self, name: str) -> Tuple[bool, str]:
        """Uninstall an extension.
        
        Args:
            name: The name of the extension to uninstall.
            
        Returns:
            A tuple containing:
            - A boolean indicating success or failure.
            - A message describing the result.
        """
        with self._lock:
            try:
                # Check if extension exists
                if name not in self.extensions:
                    return False, f"Extension {name} not found"
                
                # Get extension info
                ext_info = self.extensions[name]
                
                # Deactivate the extension if it's active
                if ext_info.status == ExtensionStatus.ACTIVE and name in self.instances:
                    instance = self.instances[name]
                    instance.deactivate()
                
                # Remove extension from registry
                del self.extensions[name]
                if name in self.instances:
                    del self.instances[name]
                
                # Uninstall the extension
                if ext_info.path:
                    success = uninstall_extension(name, self.extensions_dir)
                    if not success:
                        return False, f"Failed to uninstall extension {name}"
                
                # Save registry configuration
                self._save_config()
                
                return True, f"Extension {name} uninstalled successfully"
            except Exception as e:
                logger.error(f"Error uninstalling extension {name}: {e}")
                return False, f"Error uninstalling extension: {e}"
    
    def enable_extension(self, name: str) -> Tuple[bool, str]:
        """Enable an extension.
        
        Args:
            name: The name of the extension to enable.
            
        Returns:
            A tuple containing:
            - A boolean indicating success or failure.
            - A message describing the result.
        """
        with self._lock:
            try:
                # Check if extension exists
                if name not in self.extensions:
                    return False, f"Extension {name} not found"
                
                # Get extension info
                ext_info = self.extensions[name]
                
                # Check if extension is already active
                if ext_info.status == ExtensionStatus.ACTIVE:
                    return True, f"Extension {name} is already active"
                
                # Load the extension if not already loaded
                if name not in self.instances:
                    if not ext_info.path:
                        return False, f"Extension {name} has no path"
                    
                    init_path = os.path.join(ext_info.path, "__init__.py")
                    extension = load_extension(init_path)
                    
                    if not extension:
                        return False, f"Failed to load extension {name}"
                    
                    self.instances[name] = extension
                
                # Initialize and activate the extension
                instance = self.instances[name]
                
                # Check dependencies
                dependencies = self.get_extension_dependencies(name)
                unresolved_deps = dependencies - set(self.extensions.keys())
                
                if unresolved_deps:
                    return False, f"Extension {name} has unresolved dependencies: {', '.join(unresolved_deps)}"
                
                # Ensure all dependencies are active
                for dep_name in dependencies:
                    if dep_name in self.extensions:
                        dep_info = self.extensions[dep_name]
                        if dep_info.status != ExtensionStatus.ACTIVE:
                            # Try to enable the dependency
                            success, message = self.enable_extension(dep_name)
                            if not success:
                                return False, f"Failed to enable dependency {dep_name}: {message}"
                
                # Initialize and activate the extension
                try:
                    success = instance.initialize({})
                    if not success:
                        return False, f"Failed to initialize extension {name}"
                    
                    success = instance.activate()
                    if not success:
                        return False, f"Failed to activate extension {name}"
                    
                    # Update extension status
                    ext_info.status = ExtensionStatus.ACTIVE
                    ext_info.error = None
                    
                    # Save registry configuration
                    self._save_config()
                    
                    return True, f"Extension {name} enabled successfully"
                except Exception as e:
                    logger.error(f"Error enabling extension {name}: {e}")
                    ext_info.status = ExtensionStatus.ERROR
                    ext_info.error = str(e)
                    self._save_config()
                    return False, f"Error enabling extension: {e}"
            except Exception as e:
                logger.error(f"Error enabling extension {name}: {e}")
                return False, f"Error enabling extension: {e}"
    
    def disable_extension(self, name: str) -> Tuple[bool, str]:
        """Disable an extension.
        
        Args:
            name: The name of the extension to disable.
            
        Returns:
            A tuple containing:
            - A boolean indicating success or failure.
            - A message describing the result.
        """
        with self._lock:
            try:
                # Check if extension exists
                if name not in self.extensions:
                    return False, f"Extension {name} not found"
                
                # Get extension info
                ext_info = self.extensions[name]
                
                # Check if extension is already inactive
                if ext_info.status != ExtensionStatus.ACTIVE:
                    return True, f"Extension {name} is already inactive"
                
                # Check if other active extensions depend on this one
                dependents = self.get_extension_dependents(name)
                active_dependents = [dep for dep in dependents if self.extensions.get(dep, {}).status == ExtensionStatus.ACTIVE]
                
                if active_dependents:
                    return False, f"Extension {name} cannot be disabled because it is required by: {', '.join(active_dependents)}"
                
                # Deactivate the extension
                if name in self.instances:
                    instance = self.instances[name]
                    
                    try:
                        success = instance.deactivate()
                        if not success:
                            return False, f"Failed to deactivate extension {name}"
                    except Exception as e:
                        logger.error(f"Error deactivating extension {name}: {e}")
                        ext_info.error = str(e)
                
                # Update extension status
                ext_info.status = ExtensionStatus.INACTIVE
                
                # Save registry configuration
                self._save_config()
                
                return True, f"Extension {name} disabled successfully"
            except Exception as e:
                logger.error(f"Error disabling extension {name}: {e}")
                return False, f"Error disabling extension: {e}"
    
    def update_extension_settings(self, name: str, settings: Dict[str, Any]) -> Tuple[bool, str]:
        """Update extension settings.
        
        Args:
            name: The name of the extension.
            settings: The settings to update.
            
        Returns:
            A tuple containing:
            - A boolean indicating success or failure.
            - A message describing the result.
        """
        with self._lock:
            try:
                # Check if extension exists
                if name not in self.extensions:
                    return False, f"Extension {name} not found"
                
                # Get extension info
                ext_info = self.extensions[name]
                
                # Update settings
                for setting in ext_info.settings:
                    if setting.name in settings:
                        setting.value = settings[setting.name]
                
                # Save registry configuration
                self._save_config()
                
                # Update settings in the extension instance
                if name in self.instances:
                    instance = self.instances[name]
                    for key, value in settings.items():
                        if hasattr(instance, key):
                            setattr(instance, key, value)
                
                return True, f"Extension {name} settings updated successfully"
            except Exception as e:
                logger.error(f"Error updating extension settings: {e}")
                return False, f"Error updating extension settings: {e}"
    
    def get_extension_dependencies(self, name: str) -> Set[str]:
        """Get the names of all extensions that the given extension depends on.
        
        Args:
            name: The name of the extension.
            
        Returns:
            A set of extension names.
        """
        with self._lock:
            if name not in self.extensions:
                return set()
            
            ext_info = self.extensions[name]
            return {dep.name for dep in ext_info.dependencies}
    
    def get_extension_dependents(self, name: str) -> Set[str]:
        """Get the names of all extensions that depend on the given extension.
        
        Args:
            name: The name of the extension.
            
        Returns:
            A set of extension names.
        """
        with self._lock:
            dependents = set()
            for ext_name, ext_info in self.extensions.items():
                if ext_name != name:
                    for dep in ext_info.dependencies:
                        if dep.name == name:
                            dependents.add(ext_name)
            return dependents
    
    def initialize_all(self) -> Dict[str, Tuple[bool, str]]:
        """Initialize all extensions.
        
        Returns:
            A dictionary mapping extension names to initialization results.
        """
        with self._lock:
            # If no extensions in registry, discover them
            if not self.extensions:
                self.discover()
            
            # Get extensions that should be active
            active_extensions = [name for name, info in self.extensions.items() if info.status == ExtensionStatus.ACTIVE]
            
            # Initialize extensions in dependency order
            results = {}
            for name in active_extensions:
                success, message = self.enable_extension(name)
                results[name] = (success, message)
            
            return results

# Singleton instance for easy access
registry = ExtensionRegistry()

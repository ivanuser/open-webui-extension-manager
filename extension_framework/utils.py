"""
Utility functions for Open WebUI extensions.
"""

import os
import sys
import importlib.util
import inspect
import logging
import yaml
import json
from typing import Dict, List, Any, Type, Optional, Set, Tuple
import hashlib
import shutil
import tempfile
import zipfile
import requests
from urllib.parse import urlparse

from .base import Extension
from .decorators import register_hooks_from_instance

logger = logging.getLogger("extension_utils")

def load_extension_module(path: str) -> Optional[Any]:
    """Load an extension module from a file path.
    
    Args:
        path: The path to the extension module.
        
    Returns:
        The loaded module, or None if loading failed.
    """
    try:
        spec = importlib.util.spec_from_file_location("extension_module", path)
        if spec is None:
            logger.error(f"Failed to create module spec from {path}")
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules["extension_module"] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Failed to load extension module {path}: {e}")
        return None

def find_extension_class(module: Any) -> Optional[Type[Extension]]:
    """Find an Extension subclass in a module.
    
    Args:
        module: The module to search.
        
    Returns:
        The Extension subclass, or None if not found.
    """
    try:
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, Extension) and 
                obj != Extension and
                not inspect.isabstract(obj)):
                return obj
        logger.warning(f"No Extension subclass found in module {module.__name__}")
        return None
    except Exception as e:
        logger.error(f"Error finding extension class in module {module.__name__}: {e}")
        return None

def load_extension(path: str) -> Optional[Extension]:
    """Load an extension from a file path.
    
    Args:
        path: The path to the extension module.
        
    Returns:
        An instance of the extension, or None if loading failed.
    """
    module = load_extension_module(path)
    if module is None:
        return None
    
    extension_class = find_extension_class(module)
    if extension_class is None:
        return None
    
    try:
        extension = extension_class()
        register_hooks_from_instance(extension)
        return extension
    except Exception as e:
        logger.error(f"Error instantiating extension class {extension_class.__name__}: {e}")
        return None

def discover_extensions(directory: str) -> List[str]:
    """Discover extension modules in a directory.
    
    Args:
        directory: The directory to search.
        
    Returns:
        A list of paths to extension modules.
    """
    extension_paths = []
    
    try:
        for root, dirs, files in os.walk(directory):
            if "__init__.py" in files:
                extension_paths.append(os.path.join(root, "__init__.py"))
    except Exception as e:
        logger.error(f"Error discovering extensions in {directory}: {e}")
    
    return extension_paths

def load_extension_config(path: str) -> Dict[str, Any]:
    """Load an extension configuration from a file.
    
    Args:
        path: The path to the configuration file.
        
    Returns:
        The configuration as a dictionary.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".yaml") or path.endswith(".yml"):
                return yaml.safe_load(f) or {}
            elif path.endswith(".json"):
                return json.load(f)
            else:
                logger.warning(f"Unknown configuration file format: {path}")
                return {}
    except Exception as e:
        logger.error(f"Error loading extension configuration from {path}: {e}")
        return {}

def save_extension_config(config: Dict[str, Any], path: str) -> bool:
    """Save an extension configuration to a file.
    
    Args:
        config: The configuration to save.
        path: The path to save the configuration to.
        
    Returns:
        True if the configuration was saved successfully, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            if path.endswith(".yaml") or path.endswith(".yml"):
                yaml.dump(config, f, default_flow_style=False)
            elif path.endswith(".json"):
                json.dump(config, f, indent=2)
            else:
                logger.warning(f"Unknown configuration file format: {path}")
                return False
        return True
    except Exception as e:
        logger.error(f"Error saving extension configuration to {path}: {e}")
        return False

def hash_file(path: str) -> str:
    """Calculate the SHA-256 hash of a file.
    
    Args:
        path: The path to the file.
        
    Returns:
        The hexadecimal digest of the hash.
    """
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {path}: {e}")
        return ""

def download_file(url: str, target_path: str) -> bool:
    """Download a file from a URL.
    
    Args:
        url: The URL to download from.
        target_path: The path to save the file to.
        
    Returns:
        True if the file was downloaded successfully, False otherwise.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        logger.error(f"Error downloading file from {url}: {e}")
        return False

def install_extension_from_zip(zip_path: str, extensions_dir: str) -> Optional[str]:
    """Install an extension from a ZIP file.
    
    Args:
        zip_path: The path to the ZIP file.
        extensions_dir: The directory to install the extension to.
        
    Returns:
        The path to the installed extension, or None if installation failed.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extension directory
        extension_dir = None
        for root, dirs, files in os.walk(temp_dir):
            if "__init__.py" in files:
                extension_dir = root
                break
        
        if extension_dir is None:
            logger.error(f"No extension found in ZIP file {zip_path}")
            shutil.rmtree(temp_dir)
            return None
        
        # Load the extension to get its name
        extension = load_extension(os.path.join(extension_dir, "__init__.py"))
        if extension is None:
            logger.error(f"Failed to load extension from ZIP file {zip_path}")
            shutil.rmtree(temp_dir)
            return None
        
        # Install the extension
        target_dir = os.path.join(extensions_dir, extension.name)
        if os.path.exists(target_dir):
            logger.warning(f"Extension {extension.name} already exists, removing")
            shutil.rmtree(target_dir)
        
        shutil.copytree(extension_dir, target_dir)
        shutil.rmtree(temp_dir)
        
        return target_dir
    except Exception as e:
        logger.error(f"Error installing extension from ZIP file {zip_path}: {e}")
        if "temp_dir" in locals():
            shutil.rmtree(temp_dir)
        return None

def install_extension_from_url(url: str, extensions_dir: str) -> Optional[str]:
    """Install an extension from a URL.
    
    Args:
        url: The URL to download from.
        extensions_dir: The directory to install the extension to.
        
    Returns:
        The path to the installed extension, or None if installation failed.
    """
    try:
        # Parse the URL to get the filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename.endswith(".zip"):
            logger.error(f"URL does not point to a ZIP file: {url}")
            return None
        
        # Download the ZIP file
        temp_file = tempfile.mktemp(suffix=".zip")
        if not download_file(url, temp_file):
            return None
        
        # Install the extension from the ZIP file
        extension_path = install_extension_from_zip(temp_file, extensions_dir)
        os.remove(temp_file)
        
        return extension_path
    except Exception as e:
        logger.error(f"Error installing extension from URL {url}: {e}")
        if "temp_file" in locals() and os.path.exists(temp_file):
            os.remove(temp_file)
        return None

def install_extension_from_directory(source_dir: str, extensions_dir: str) -> Optional[str]:
    """Install an extension from a directory.
    
    Args:
        source_dir: The source directory.
        extensions_dir: The directory to install the extension to.
        
    Returns:
        The path to the installed extension, or None if installation failed.
    """
    try:
        # Check if the source directory contains an extension
        if not os.path.exists(os.path.join(source_dir, "__init__.py")):
            logger.error(f"No extension found in directory {source_dir}")
            return None
        
        # Load the extension to get its name
        extension = load_extension(os.path.join(source_dir, "__init__.py"))
        if extension is None:
            logger.error(f"Failed to load extension from directory {source_dir}")
            return None
        
        # Install the extension
        target_dir = os.path.join(extensions_dir, extension.name)
        if os.path.exists(target_dir):
            logger.warning(f"Extension {extension.name} already exists, removing")
            shutil.rmtree(target_dir)
        
        shutil.copytree(source_dir, target_dir)
        
        return target_dir
    except Exception as e:
        logger.error(f"Error installing extension from directory {source_dir}: {e}")
        return None

def uninstall_extension(extension_name: str, extensions_dir: str) -> bool:
    """Uninstall an extension.
    
    Args:
        extension_name: The name of the extension to uninstall.
        extensions_dir: The directory containing the extensions.
        
    Returns:
        True if the extension was uninstalled successfully, False otherwise.
    """
    try:
        extension_dir = os.path.join(extensions_dir, extension_name)
        if not os.path.exists(extension_dir):
            logger.error(f"Extension {extension_name} not found in {extensions_dir}")
            return False
        
        shutil.rmtree(extension_dir)
        return True
    except Exception as e:
        logger.error(f"Error uninstalling extension {extension_name}: {e}")
        return False

def get_extension_dependencies(extension: Extension) -> Set[str]:
    """Get the names of all extensions that the given extension depends on.
    
    Args:
        extension: The extension to get dependencies for.
        
    Returns:
        A set of extension names.
    """
    return set(extension.dependencies)

def resolve_extension_dependencies(extensions: List[Extension]) -> List[Tuple[Extension, Set[str]]]:
    """Resolve dependencies between extensions.
    
    Args:
        extensions: A list of extensions.
        
    Returns:
        A list of tuples containing the extension and its unresolved dependencies.
    """
    # Create a dictionary mapping extension names to extensions
    extension_map = {ext.name: ext for ext in extensions}
    
    # Create a dictionary mapping extension names to unresolved dependencies
    unresolved_deps = {}
    for ext in extensions:
        deps = get_extension_dependencies(ext)
        unresolved = deps - set(extension_map.keys())
        unresolved_deps[ext.name] = unresolved
    
    # Return extensions with their unresolved dependencies
    return [(ext, unresolved_deps[ext.name]) for ext in extensions]

def sort_extensions_by_dependencies(extensions: List[Extension]) -> List[Extension]:
    """Sort extensions by their dependencies.
    
    Args:
        extensions: A list of extensions.
        
    Returns:
        A list of extensions sorted by their dependencies.
    """
    # Create a dictionary mapping extension names to extensions
    extension_map = {ext.name: ext for ext in extensions}
    
    # Create a dictionary mapping extension names to dependencies
    deps = {ext.name: get_extension_dependencies(ext) for ext in extensions}
    
    # Sort extensions by dependencies
    sorted_names = []
    visited = set()
    
    def visit(name):
        if name in visited:
            return
        visited.add(name)
        for dep in deps.get(name, set()):
            if dep in extension_map:
                visit(dep)
        sorted_names.append(name)
    
    for ext in extensions:
        visit(ext.name)
    
    # Return extensions in dependency order
    return [extension_map[name] for name in sorted_names]

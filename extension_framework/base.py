"""
Base classes for Open WebUI extensions.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Type
import inspect
import os
import logging

logger = logging.getLogger("extension_framework")

class Extension(ABC):
    """Base class for all extensions."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the extension."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the extension."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the extension does."""
        pass
    
    @property
    @abstractmethod
    def author(self) -> str:
        """The author(s) of the extension."""
        pass
    
    @property
    def dependencies(self) -> List[str]:
        """List of other extensions this extension depends on."""
        return []
    
    @property
    def type(self) -> str:
        """The type of extension (UI, API, Model, Tool, Theme)."""
        return "generic"
    
    @property
    def settings(self) -> Dict[str, Any]:
        """The extension's default settings."""
        return {}
    
    @property
    def static_dir(self) -> Optional[str]:
        """The directory containing static files for this extension."""
        module_dir = os.path.dirname(inspect.getmodule(self).__file__)
        static_path = os.path.join(module_dir, "static")
        return static_path if os.path.exists(static_path) else None
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the extension with the given context.
        
        Args:
            context: A dictionary containing context information for initialization.
            
        Returns:
            True if initialization was successful, False otherwise.
        """
        logger.info(f"Initializing extension: {self.name}")
        return True
    
    def activate(self) -> bool:
        """Activate the extension.
        
        Returns:
            True if activation was successful, False otherwise.
        """
        logger.info(f"Activating extension: {self.name}")
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension.
        
        Returns:
            True if deactivation was successful, False otherwise.
        """
        logger.info(f"Deactivating extension: {self.name}")
        return True
    
    def uninstall(self) -> bool:
        """Perform cleanup when uninstalling the extension.
        
        Returns:
            True if uninstallation was successful, False otherwise.
        """
        logger.info(f"Uninstalling extension: {self.name}")
        return True

class UIExtension(Extension):
    """Base class for UI extensions."""
    
    @property
    def type(self) -> str:
        return "ui"
    
    @property
    @abstractmethod
    def components(self) -> Dict[str, Any]:
        """A dictionary of UI components provided by this extension."""
        pass
    
    @property
    def mount_points(self) -> Dict[str, List[str]]:
        """A dictionary mapping mount points to component IDs."""
        return {}

class APIExtension(Extension):
    """Base class for API extensions."""
    
    @property
    def type(self) -> str:
        return "api"
    
    @property
    @abstractmethod
    def routes(self) -> List[Any]:
        """A list of API routes provided by this extension."""
        pass

class ModelAdapter(Extension):
    """Base class for model adapter extensions."""
    
    @property
    def type(self) -> str:
        return "model"
    
    @abstractmethod
    def load_model(self) -> Any:
        """Load the AI model."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generate a response from the model.
        
        Args:
            prompt: The input prompt.
            params: Generation parameters.
            
        Returns:
            The generated text.
        """
        pass

class ToolExtension(Extension):
    """Base class for tool extensions."""
    
    @property
    def type(self) -> str:
        return "tool"
    
    @property
    @abstractmethod
    def tools(self) -> Dict[str, Callable]:
        """A dictionary of tools provided by this extension."""
        pass

class ThemeExtension(Extension):
    """Base class for theme extensions."""
    
    @property
    def type(self) -> str:
        return "theme"
    
    @property
    @abstractmethod
    def styles(self) -> Dict[str, str]:
        """A dictionary of style definitions."""
        pass
    
    @property
    @abstractmethod
    def theme_name(self) -> str:
        """The name of the theme."""
        pass

def get_extension_class(extension_type: str) -> Type[Extension]:
    """Get the appropriate extension class based on the type.
    
    Args:
        extension_type: The type of extension.
        
    Returns:
        The extension class.
    """
    extension_classes = {
        "ui": UIExtension,
        "api": APIExtension,
        "model": ModelAdapter,
        "tool": ToolExtension,
        "theme": ThemeExtension,
        "generic": Extension,
    }
    return extension_classes.get(extension_type, Extension)

"""
Open WebUI Extension Framework

This module provides the framework for creating and managing extensions for Open WebUI.
"""

"""
Extension Framework for Open WebUI.

This framework provides the foundation for building extensions for Open WebUI.
"""

from .base import (
    Extension,
    UIExtension,
    APIExtension,
    ModelAdapter,
    ToolExtension,
    ThemeExtension,
    get_extension_class,
)

from .hooks import (
    register_hook,
    register_callback,
    unregister_callback,
    execute_hook,
    get_hooks,
    get_callbacks,
)

from .decorators import (
    hook,
    ui_component,
    api_route,
    tool,
    setting,
    register_hooks_from_instance,
    collect_components_from_instance,
    collect_routes_from_instance,
    collect_tools_from_instance,
    collect_settings_from_class,
)

from .utils import (
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

__all__ = [
    # Base classes
    "Extension",
    "UIExtension",
    "APIExtension",
    "ModelAdapter",
    "ToolExtension",
    "ThemeExtension",
    "get_extension_class",
    
    # Hooks
    "register_hook",
    "register_callback",
    "unregister_callback",
    "execute_hook",
    "get_hooks",
    "get_callbacks",
    
    # Decorators
    "hook",
    "ui_component",
    "api_route",
    "tool",
    "setting",
    "register_hooks_from_instance",
    "collect_components_from_instance",
    "collect_routes_from_instance",
    "collect_tools_from_instance",
    "collect_settings_from_class",
    
    # Utilities
    "load_extension",
    "discover_extensions",
    "load_extension_config",
    "save_extension_config",
    "install_extension_from_zip",
    "install_extension_from_url",
    "install_extension_from_directory",
    "uninstall_extension",
    "resolve_extension_dependencies",
    "sort_extensions_by_dependencies",
]

__version__ = "0.1.0"

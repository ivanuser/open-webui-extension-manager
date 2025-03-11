"""
Decorators for Open WebUI extensions.
"""

from typing import Callable, Any, Dict, List, Optional, Type, Union
from functools import wraps
import inspect

from .hooks import register_callback

def hook(hook_name: str, priority: int = 10):
    """Decorator to register a function as a hook callback.
    
    Args:
        hook_name: The name of the hook to register for.
        priority: The priority of the callback (lower numbers run first).
        
    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        # Store the hook information in the function
        if not hasattr(func, "_hook_info"):
            func._hook_info = []
        
        func._hook_info.append({
            "hook_name": hook_name,
            "priority": priority,
        })
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def ui_component(component_id: str, mount_points: List[str] = None):
    """Decorator to register a function as a UI component.
    
    Args:
        component_id: The ID of the component.
        mount_points: A list of mount points for the component.
        
    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        # Store the component information in the function
        if not hasattr(func, "_component_info"):
            func._component_info = {}
        
        func._component_info["id"] = component_id
        func._component_info["mount_points"] = mount_points or []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def api_route(path: str, methods: List[str] = None, tags: List[str] = None, summary: str = None, response_model: Type = None):
    """Decorator to register a function as an API route.
    
    Args:
        path: The URL path for the route.
        methods: A list of HTTP methods for the route.
        tags: A list of tags for the route.
        summary: A summary of the route.
        response_model: The response model for the route.
        
    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        # Store the route information in the function
        if not hasattr(func, "_route_info"):
            func._route_info = {}
        
        func._route_info["path"] = path
        func._route_info["methods"] = methods or ["GET"]
        func._route_info["tags"] = tags or []
        func._route_info["summary"] = summary
        func._route_info["response_model"] = response_model
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def tool(name: str, description: str = None):
    """Decorator to register a function as a tool.
    
    Args:
        name: The name of the tool.
        description: A description of the tool.
        
    Returns:
        A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        # Store the tool information in the function
        if not hasattr(func, "_tool_info"):
            func._tool_info = {}
        
        func._tool_info["name"] = name
        func._tool_info["description"] = description or func.__doc__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator

def setting(
    name: str, 
    default: Any = None, 
    type_: Type = None, 
    description: str = None, 
    options: List[Dict[str, Any]] = None,
    required: bool = False,
    category: str = "General"
):
    """Decorator to register a class attribute as a setting.
    
    Args:
        name: The name of the setting.
        default: The default value of the setting.
        type_: The type of the setting.
        description: A description of the setting.
        options: A list of options for the setting.
        required: Whether the setting is required.
        category: The category of the setting.
        
    Returns:
        A decorator function.
    """
    def decorator(cls: Type) -> Type:
        # Store the setting information in the class
        if not hasattr(cls, "_settings_info"):
            cls._settings_info = []
        
        # Get the type from the default value if not provided
        inferred_type = type_ or type(default) if default is not None else str
        
        cls._settings_info.append({
            "name": name,
            "default": default,
            "type": inferred_type.__name__,
            "description": description,
            "options": options,
            "required": required,
            "category": category,
        })
        
        return cls
    
    return decorator

def register_hooks_from_instance(instance: Any) -> None:
    """Register all hook callbacks from an instance.
    
    Args:
        instance: The instance to register hooks from.
    """
    for name, method in inspect.getmembers(instance, inspect.ismethod):
        if hasattr(method, "_hook_info"):
            for hook_info in method._hook_info:
                register_callback(
                    hook_info["hook_name"],
                    method,
                    instance.name,
                    hook_info["priority"]
                )

def collect_components_from_instance(instance: Any) -> Dict[str, Dict[str, Any]]:
    """Collect all UI components from an instance.
    
    Args:
        instance: The instance to collect components from.
        
    Returns:
        A dictionary of component information.
    """
    components = {}
    
    for name, method in inspect.getmembers(instance, inspect.ismethod):
        if hasattr(method, "_component_info"):
            component_info = method._component_info
            components[component_info["id"]] = {
                "render": method,
                "mount_points": component_info["mount_points"],
            }
    
    return components

def collect_routes_from_instance(instance: Any) -> List[Dict[str, Any]]:
    """Collect all API routes from an instance.
    
    Args:
        instance: The instance to collect routes from.
        
    Returns:
        A list of route information.
    """
    routes = []
    
    for name, method in inspect.getmembers(instance, inspect.ismethod):
        if hasattr(method, "_route_info"):
            route_info = method._route_info.copy()
            route_info["endpoint"] = method
            routes.append(route_info)
    
    return routes

def collect_tools_from_instance(instance: Any) -> Dict[str, Dict[str, Any]]:
    """Collect all tools from an instance.
    
    Args:
        instance: The instance to collect tools from.
        
    Returns:
        A dictionary of tool information.
    """
    tools = {}
    
    for name, method in inspect.getmembers(instance, inspect.ismethod):
        if hasattr(method, "_tool_info"):
            tool_info = method._tool_info
            tools[tool_info["name"]] = {
                "function": method,
                "description": tool_info["description"],
            }
    
    return tools

def collect_settings_from_class(cls: Type) -> List[Dict[str, Any]]:
    """Collect all settings from a class.
    
    Args:
        cls: The class to collect settings from.
        
    Returns:
        A list of setting information.
    """
    if hasattr(cls, "_settings_info"):
        return cls._settings_info
    return []

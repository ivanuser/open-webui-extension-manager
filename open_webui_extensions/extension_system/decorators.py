from typing import Callable, List, Dict, Any, Optional, Type
import functools
import inspect

from .hooks import hook_manager

def startup_hook(func: Callable) -> Callable:
    """Decorator for functions to be called on startup."""
    hook_manager.register_hook('on_startup', func)
    return func

def shutdown_hook(func: Callable) -> Callable:
    """Decorator for functions to be called on shutdown."""
    hook_manager.register_hook('on_shutdown', func)
    return func

def chat_request_hook(func: Callable) -> Callable:
    """Decorator for functions to be called before a chat request."""
    hook_manager.register_hook('on_chat_request', func)
    return func

def chat_response_hook(func: Callable) -> Callable:
    """Decorator for functions to be called after a chat response."""
    hook_manager.register_hook('on_chat_response', func)
    return func

def ui_component(location: str, order: int = 0):
    """Decorator for UI components."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._ui_component = True
        wrapper._ui_location = location
        wrapper._ui_order = order
        hook_manager.register_hook('on_ui_tab', wrapper)
        
        return wrapper
    return decorator

def api_route(path: str, methods: List[str] = ["GET"]):
    """Decorator for API endpoints."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._api_route = True
        wrapper._api_path = path
        wrapper._api_methods = methods
        hook_manager.register_hook('on_api_route', wrapper)
        
        return wrapper
    return decorator

def tool(name: str, description: str):
    """Decorator for tools."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._tool = True
        wrapper._tool_name = name
        wrapper._tool_description = description
        hook_manager.register_hook('on_tool', wrapper)
        
        return wrapper
    return decorator

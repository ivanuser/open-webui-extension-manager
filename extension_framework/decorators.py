"""
Decorators for Open WebUI extensions.
"""

from typing import List, Callable, Dict, Any, Type, TypeVar
from functools import wraps

# Type definitions
T = TypeVar('T')
HookFunction = Callable[..., Any]


def hook(hook_name: str):
    """Decorator to register a hook callback."""
    def decorator(func: HookFunction) -> HookFunction:
        func._hook_name = hook_name
        return func
    return decorator


def api_route(path: str, methods: List[str] = ["GET"], **kwargs):
    """Decorator to register an API route."""
    def decorator(func: Callable) -> Callable:
        func._api_route = {
            "path": path,
            "methods": methods,
            **kwargs
        }
        return func
    return decorator


def admin_page(title: str, icon: str, path: str):
    """Decorator to register an admin page."""
    def decorator(cls: Type[T]) -> Type[T]:
        cls.admin_page = {
            "title": title,
            "icon": icon,
            "path": path
        }
        return cls
    return decorator


def sidebar_item(title: str, icon: str, path: str):
    """Decorator to register a sidebar item."""
    def decorator(cls: Type[T]) -> Type[T]:
        if not hasattr(cls, "sidebar_items"):
            cls.sidebar_items = []
        cls.sidebar_items.append({
            "title": title,
            "icon": icon,
            "path": path
        })
        return cls
    return decorator


def settings_section(title: str, icon: str, component: str):
    """Decorator to register a settings section."""
    def decorator(cls: Type[T]) -> Type[T]:
        if not hasattr(cls, "settings_sections"):
            cls.settings_sections = []
        cls.settings_sections.append({
            "title": title,
            "icon": icon,
            "component": component
        })
        return cls
    return decorator

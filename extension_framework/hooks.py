"""
Hook system for Open WebUI extensions.
"""

import inspect
import logging
from typing import Dict, List, Any, Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui.extensions.hooks")

# Type definitions
HookFunction = Callable[..., Any]
HookRegistry = Dict[str, List[HookFunction]]

# Global hook registry
_hooks: HookRegistry = {}


def register_hook(hook_name: str, callback: HookFunction) -> None:
    """Register a hook callback."""
    global _hooks
    
    if hook_name not in _hooks:
        _hooks[hook_name] = []
    
    _hooks[hook_name].append(callback)
    logger.debug(f"Registered hook '{hook_name}'")


async def call_hook(hook_name: str, *args, **kwargs) -> List[Any]:
    """Call all registered callbacks for a hook."""
    global _hooks
    
    if hook_name not in _hooks:
        return []
    
    results = []
    for callback in _hooks[hook_name]:
        try:
            if inspect.iscoroutinefunction(callback):
                result = await callback(*args, **kwargs)
            else:
                result = callback(*args, **kwargs)
            
            results.append(result)
        except Exception as e:
            logger.error(f"Error in hook '{hook_name}': {e}")
    
    return results


def get_hooks() -> HookRegistry:
    """Get all registered hooks."""
    global _hooks
    return _hooks


def clear_hooks() -> None:
    """Clear all registered hooks."""
    global _hooks
    _hooks = {}

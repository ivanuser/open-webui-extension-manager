from typing import Dict, List, Callable, Any
import logging
import inspect
import asyncio

logger = logging.getLogger("open_webui_extensions")

class HookManager:
    """Manages extension hooks."""
    
    _instance = None
    hooks: Dict[str, List[Callable]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HookManager, cls).__new__(cls)
            cls._instance.hooks = {
                'on_startup': [],
                'on_shutdown': [],
                'on_chat_request': [],
                'on_chat_response': [],
                'on_ui_tab': [],
                'on_api_route': [],
                'on_tool': [],
            }
        return cls._instance
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a callback for a specific hook."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        if callback not in self.hooks[hook_name]:
            self.hooks[hook_name].append(callback)
    
    def unregister_hook(self, hook_name: str, callback: Callable) -> None:
        """Unregister a callback for a specific hook."""
        if hook_name in self.hooks and callback in self.hooks[hook_name]:
            self.hooks[hook_name].remove(callback)
    
    async def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all callbacks for a specific hook."""
        results = []
        
        if hook_name not in self.hooks:
            return results
        
        for callback in self.hooks[hook_name]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    result = await callback(*args, **kwargs)
                else:
                    result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Error triggering hook {hook_name}: {str(e)}")
        
        return results
    
    def clear_hooks(self, hook_name: str = None) -> None:
        """Clear all hooks or hooks for a specific name."""
        if hook_name:
            if hook_name in self.hooks:
                self.hooks[hook_name] = []
        else:
            for hook_name in self.hooks:
                self.hooks[hook_name] = []

# Singleton instance
hook_manager = HookManager()

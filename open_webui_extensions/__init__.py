"""Open WebUI Extension System."""

from .extension_system.base import (
    Extension,
    UIExtension,
    APIExtension,
    ModelAdapterExtension,
    ToolExtension,
    ThemeExtension,
)
from .extension_system.decorators import (
    startup_hook,
    shutdown_hook,
    chat_request_hook,
    chat_response_hook,
    ui_component,
    api_route,
    tool,
)
from .extension_system.hooks import hook_manager
from .extension_system.registry import extension_registry
from .plugin import on_startup, on_shutdown

__version__ = "0.1.0"

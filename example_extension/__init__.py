"""
Example Extension for Open WebUI

This is an example extension that demonstrates how to use the Open WebUI extension framework.
It provides a simple UI dashboard and API endpoints to showcase extension capabilities.

id: example_extension
name: Example Extension
description: Example extension for Open WebUI that demonstrates extension capabilities
version: 0.1.0
author: Open WebUI Team
author_url: https://github.com/open-webui
repository_url: https://github.com/open-webui/extensions
license: MIT
tags: [example, demo, tutorial]
"""

import logging
from typing import Dict, List, Any

from extension_framework import (
    UIExtension,
    hook,
    ui_component,
    setting,
)

logger = logging.getLogger("example_extension")

@setting(name="greeting_text", default="Hello from Example Extension!", description="Text to display in the greeting")
@setting(name="greeting_color", default="#007bff", description="Color of the greeting text")
@setting(name="show_greeting", default=True, type_=bool, description="Whether to show the greeting")
class ExampleExtension(UIExtension):
    """A simple example extension."""
    
    @property
    def name(self) -> str:
        return "example-extension"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    @property
    def description(self) -> str:
        return "A simple example extension to demonstrate how to build extensions."
    
    @property
    def author(self) -> str:
        return "Open WebUI Team"
    
    @property
    def components(self) -> Dict[str, Any]:
        from .ui import get_components
        return get_components()
    
    @property
    def mount_points(self) -> Dict[str, List[str]]:
        return {
            "sidebar": ["example_greeting"],
            "chat": ["example_helper"],
        }
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the extension."""
        logger.info("Initializing example extension")
        # You can perform initialization tasks here, such as:
        # - Loading configuration
        # - Connecting to external services
        # - Registering hooks
        return True
    
    def activate(self) -> bool:
        """Activate the extension."""
        logger.info("Activating example extension")
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension."""
        logger.info("Deactivating example extension")
        return True
    
    @hook("ui_init")
    def on_ui_init(self) -> None:
        """Hook called when the UI is initialized."""
        logger.info("UI initialized")
    
    @hook("ui_chat")
    def on_ui_chat(self, chat_id: str) -> None:
        """Hook called when the chat interface is rendered."""
        logger.info(f"Chat interface rendered: {chat_id}")
    
    @hook("model_before_generate", priority=5)
    def on_model_before_generate(self, prompt: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before generating text."""
        logger.info(f"Generating text with prompt: {prompt[:50]}...")
        # You can modify the prompt or parameters here
        return params

# Create an instance of the extension
extension = ExampleExtension()

"""
UI components for the example extension.
"""

from typing import Dict, Any, List

from extension_framework import ui_component

@ui_component("example_greeting", mount_points=["sidebar"])
def render_greeting(extension) -> Dict[str, Any]:
    """Render a greeting in the sidebar."""
    if not extension.show_greeting:
        return {"html": ""}
    
    return {
        "html": f"""
        <div class="example-extension-greeting" style="color: {extension.greeting_color}; padding: 1rem; text-align: center; font-weight: bold;">
            {extension.greeting_text}
        </div>
        """
    }

@ui_component("example_helper", mount_points=["chat"])
def render_helper(extension) -> Dict[str, Any]:
    """Render a helper in the chat interface."""
    return {
        "html": f"""
        <div class="example-extension-helper" style="margin: 0.5rem 0; padding: 0.5rem; background-color: #f8f9fa; border-radius: 0.25rem; font-size: 0.875rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <div style="font-weight: bold;">Example Extension Helper</div>
                <button id="example-helper-toggle" style="background: none; border: none; cursor: pointer; font-size: 0.75rem; color: #007bff;">Show Tips</button>
            </div>
            <div id="example-helper-content" style="display: none; margin-top: 0.5rem;">
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Use <strong>/help</strong> to see available commands</li>
                    <li>Try asking about <strong>"the weather"</strong> for a demo</li>
                    <li>Click <strong>"Example Extension"</strong> in settings to configure</li>
                </ul>
            </div>
        </div>
        
        <script>
            document.getElementById('example-helper-toggle').addEventListener('click', function() {
                const content = document.getElementById('example-helper-content');
                const isVisible = content.style.display !== 'none';
                content.style.display = isVisible ? 'none' : 'block';
                this.textContent = isVisible ? 'Show Tips' : 'Hide Tips';
            });
        </script>
        """
    }

def get_components() -> Dict[str, Any]:
    """Get all UI components for the extension."""
    return {
        "example_greeting": render_greeting,
        "example_helper": render_helper,
    }

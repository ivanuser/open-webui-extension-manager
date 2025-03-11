# Extension API Reference

This document provides a reference for the Extension API in Open WebUI.

## Table of Contents

- [Base Classes](#base-classes)
- [Hooks](#hooks)
- [Decorators](#decorators)
- [Utilities](#utilities)

## Base Classes

### Extension

The base class for all extensions.

```python
class Extension(ABC):
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
        """Initialize the extension with the given context."""
        return True
    
    def activate(self) -> bool:
        """Activate the extension."""
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension."""
        return True
    
    def uninstall(self) -> bool:
        """Perform cleanup when uninstalling the extension."""
        return True
```

### UIExtension

Base class for UI extensions.

```python
class UIExtension(Extension):
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
```

### APIExtension

Base class for API extensions.

```python
class APIExtension(Extension):
    @property
    def type(self) -> str:
        return "api"
    
    @property
    @abstractmethod
    def routes(self) -> List[Any]:
        """A list of API routes provided by this extension."""
        pass
```

### ModelAdapter

Base class for model adapter extensions.

```python
class ModelAdapter(Extension):
    @property
    def type(self) -> str:
        return "model"
    
    @abstractmethod
    def load_model(self) -> Any:
        """Load the AI model."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generate a response from the model."""
        pass
```

### ToolExtension

Base class for tool extensions.

```python
class ToolExtension(Extension):
    @property
    def type(self) -> str:
        return "tool"
    
    @property
    @abstractmethod
    def tools(self) -> Dict[str, Callable]:
        """A dictionary of tools provided by this extension."""
        pass
```

### ThemeExtension

Base class for theme extensions.

```python
class ThemeExtension(Extension):
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
```

## Hooks

The extension system provides a hook system that allows extensions to integrate with Open WebUI at specific points in the application's lifecycle.

### Available Hooks

#### UI Hooks

- `ui_init`: Called when the UI is initialized
- `ui_render`: Called when the UI is rendered
- `ui_sidebar`: Called when the sidebar is rendered
- `ui_header`: Called when the header is rendered
- `ui_footer`: Called when the footer is rendered
- `ui_chat`: Called when the chat interface is rendered
- `ui_settings`: Called when the settings page is rendered

#### API Hooks

- `api_init`: Called when the API is initialized
- `api_register_routes`: Called when API routes are registered
- `api_before_request`: Called before processing an API request
- `api_after_request`: Called after processing an API request

#### Model Hooks

- `model_init`: Called when a model is initialized
- `model_register`: Called when a model is registered
- `model_before_generate`: Called before generating text
- `model_after_generate`: Called after generating text

#### System Hooks

- `system_init`: Called when the system is initialized
- `system_shutdown`: Called when the system is shut down
- `system_settings_load`: Called when system settings are loaded
- `system_settings_save`: Called when system settings are saved

### Registering Hooks

You can register hooks using the `@hook` decorator:

```python
from extension_framework import hook

@hook("ui_init")
def on_ui_init(self) -> None:
    """Hook called when the UI is initialized."""
    logging.info("UI initialized")

@hook("model_before_generate", priority=5)
def on_model_before_generate(self, prompt: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Hook called before generating text."""
    logging.info(f"Generating text with prompt: {prompt[:50]}...")
    # You can modify the prompt or parameters here
    return params
```

## Decorators

The extension system provides several decorators to simplify extension development.

### @hook

Register a method as a hook handler.

```python
@hook(hook_name: str, priority: int = 10)
```

Arguments:
- `hook_name`: The name of the hook to register for
- `priority`: The priority of the handler (lower numbers run first)

### @ui_component

Register a method as a UI component.

```python
@ui_component(component_id: str, mount_points: List[str] = None)
```

Arguments:
- `component_id`: The ID of the component
- `mount_points`: A list of mount points for the component

### @api_route

Register a method as an API route.

```python
@api_route(path: str, methods: List[str] = None, tags: List[str] = None, summary: str = None, response_model: Type = None)
```

Arguments:
- `path`: The URL path for the route
- `methods`: A list of HTTP methods for the route
- `tags`: A list of tags for the route
- `summary`: A summary of the route
- `response_model`: The response model for the route

### @tool

Register a method as a tool.

```python
@tool(name: str, description: str = None)
```

Arguments:
- `name`: The name of the tool
- `description`: A description of the tool

### @setting

Register a class attribute as a setting.

```python
@setting(name: str, default: Any = None, type_: Type = None, description: str = None, options: List[Dict[str, Any]] = None, required: bool = False, category: str = "General")
```

Arguments:
- `name`: The name of the setting
- `default`: The default value of the setting
- `type_`: The type of the setting
- `description`: A description of the setting
- `options`: A list of options for the setting
- `required`: Whether the setting is required
- `category`: The category of the setting

## Utilities

The extension system provides several utility functions to simplify extension development.

### load_extension

Load an extension from a file path.

```python
load_extension(path: str) -> Optional[Extension]
```

Arguments:
- `path`: The path to the extension module

Returns:
- An instance of the extension, or None if loading failed

### discover_extensions

Discover extension modules in a directory.

```python
discover_extensions(directory: str) -> List[str]
```

Arguments:
- `directory`: The directory to search

Returns:
- A list of paths to extension modules

### load_extension_config

Load an extension configuration from a file.

```python
load_extension_config(path: str) -> Dict[str, Any]
```

Arguments:
- `path`: The path to the configuration file

Returns:
- The configuration as a dictionary

### save_extension_config

Save an extension configuration to a file.

```python
save_extension_config(config: Dict[str, Any], path: str) -> bool
```

Arguments:
- `config`: The configuration to save
- `path`: The path to save the configuration to

Returns:
- True if the configuration was saved successfully, False otherwise

### install_extension_from_zip

Install an extension from a ZIP file.

```python
install_extension_from_zip(zip_path: str, extensions_dir: str) -> Optional[str]
```

Arguments:
- `zip_path`: The path to the ZIP file
- `extensions_dir`: The directory to install the extension to

Returns:
- The path to the installed extension, or None if installation failed

### install_extension_from_url

Install an extension from a URL.

```python
install_extension_from_url(url: str, extensions_dir: str) -> Optional[str]
```

Arguments:
- `url`: The URL to download from
- `extensions_dir`: The directory to install the extension to

Returns:
- The path to the installed extension, or None if installation failed

### install_extension_from_directory

Install an extension from a directory.

```python
install_extension_from_directory(source_dir: str, extensions_dir: str) -> Optional[str]
```

Arguments:
- `source_dir`: The source directory
- `extensions_dir`: The directory to install the extension to

Returns:
- The path to the installed extension, or None if installation failed

### uninstall_extension

Uninstall an extension.

```python
uninstall_extension(extension_name: str, extensions_dir: str) -> bool
```

Arguments:
- `extension_name`: The name of the extension to uninstall
- `extensions_dir`: The directory containing the extensions

Returns:
- True if the extension was uninstalled successfully, False otherwise

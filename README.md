```markdown
# Open WebUI Extension System

The Open WebUI Extension System provides a framework for developing, installing, and managing extensions for Open WebUI.

## Features

-   **Extension Manager with admin interface:** Easily manage extensions through a user-friendly interface.
-   **API for extensions to integrate with Open WebUI:** Enables seamless integration and communication between extensions and the core application.
-   **Support for diverse extension types:**
    -   UI Extensions: Modify and enhance the user interface.
    -   API Extensions: Extend the API capabilities.
    -   Model Adapters: Integrate different machine learning models.
    -   Tool Extensions: Add new tools and functionalities.
    -   Theme Extensions: Customize the look and feel of Open WebUI.
-   **CLI tool for extension management:** Manage extensions directly from the command line.

## Installation

### Installing with pip

```bash
pip install open-webui-extensions
```

### Installing from source

```bash
git clone [https://github.com/yourusername/open-webui-extension-manager.git](https://github.com/yourusername/open-webui-extension-manager.git)
cd open-webui-extension-manager
pip install -e .
```

### Setting Up

1.  **Set up the extension system:**

    ```bash
    openwebui-ext setup
    ```

2.  **Install the admin integration (for Open WebUI integration):**

    ```bash
    python -m open_webui_extensions.install_openwebui
    ```

## Usage

### Extension Manager UI

-   **Integrated with the Open WebUI admin interface:** `/admin/extensions`
-   **Standalone interface:** `/api/_extensions/ui`

### CLI Tool

```bash
# List installed extensions
openwebui-ext list

# Install an extension (from a local path)
openwebui-ext install /path/to/extension

# Enable an extension
openwebui-ext enable extension_id

# Disable an extension
openwebui-ext disable extension_id

# Uninstall an extension
openwebui-ext uninstall extension_id

# Run the development server
openwebui-ext dev-server
```

## Creating Extensions

See the [documentation](link_to_documentation_here) for information on creating extensions.

## API Reference

See the [API reference](link_to_api_reference_here) for information on the extension API.

## License

MIT

## Phase 9: Integration and Testing

### Step 1: Test the Extension System

1.  **Install the extension system:**

    ```bash
    cd open-webui-extension-manager
    pip install -e .
    ```

2.  **Set up the extension system:**

    ```bash
    openwebui-ext setup
    ```

3.  **Install the example extensions:**

    ```bash
    openwebui-ext install example_extensions/hello_world
    openwebui-ext install example_extensions/weather_tool
    ```

4.  **Enable the example extensions:**

    ```bash
    openwebui-ext enable hello_world
    openwebui-ext enable weather_tool
    ```

5.  **Run the development server:**

    ```bash
    openwebui-ext dev-server
    ```

6.  **Access the Extension Manager UI:** `http://localhost:8000/api/_extensions/ui/`

### Step 2: Integrate with Open WebUI

1.  **Install the admin integration:**

    ```bash
    python -m open_webui_extensions.install_openwebui
    ```

2.  **Restart Open WebUI.**

3.  **Access the Extension Manager:** `http://localhost:8080/admin/extensions` (adjust the port as needed).
```

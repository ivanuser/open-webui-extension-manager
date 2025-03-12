# Open WebUI Extension System

The Open WebUI Extension System provides a framework for developing, installing, and managing extensions for Open WebUI.

## Features

- Extension Manager with admin interface
- API for extensions to integrate with Open WebUI
- Support for different types of extensions:
  - UI Extensions
  - API Extensions
  - Model Adapters
  - Tool Extensions
  - Theme Extensions
- CLI tool for extension management

## Installation

### Installing with pip

```bash
pip install open-webui-extensions
Installing from source
bashCopygit clone https://github.com/yourusername/open-webui-extension-manager.git
cd open-webui-extension-manager
pip install -e .
Setting Up

Set up the extension system:

bashCopyopenwebui-ext setup

Install the admin integration:

bashCopypython -m open_webui_extensions.install_openwebui
Usage
Extension Manager UI
Access the Extension Manager at:

/admin/extensions - Integrated with the Open WebUI admin interface
/api/_extensions/ui - Standalone interface

CLI Tool
bashCopy# List installed extensions
openwebui-ext list

# Install an extension
openwebui-ext install /path/to/extension

# Enable an extension
openwebui-ext enable extension_id

# Disable an extension
openwebui-ext disable extension_id

# Uninstall an extension
openwebui-ext uninstall extension_id

# Run the development server
openwebui-ext dev-server
Creating Extensions
See the documentation for information on creating extensions.
API Reference
See the API reference for information on the extension API.
License
MIT
Copy
## Phase 9: Integration and Testing

### Step 1: Test the Extension System

1. Install the extension system:

```bash
cd open-webui-extension-manager
pip install -e .

Set up the extension system:

bashCopyopenwebui-ext setup

Install the example extensions:

bashCopyopenwebui-ext install example_extensions/hello_world
openwebui-ext install example_extensions/weather_tool

Enable the example extensions:

bashCopyopenwebui-ext enable hello_world
openwebui-ext enable weather_tool

Run the development server:

bashCopyopenwebui-ext dev-server

Access the Extension Manager UI at http://localhost:8000/api/_extensions/ui/

Step 2: Integrate with Open WebUI

Install the admin integration:

bashCopypython -m open_webui_extensions.install_openwebui

Restart Open WebUI.
Access the Extension Manager at http://localhost:8080/admin/extensions (adjust the port as needed).

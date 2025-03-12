# Extension Manager

The Extension Manager provides an admin interface for managing extensions in Open WebUI.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Using the Extension Manager](#using-the-extension-manager)
- [Extension Manager API](#extension-manager-api)
- [Architecture](#architecture)

## Features

- View installed extensions
- Enable/disable extensions
- Install new extensions
- Configure extension settings
- Uninstall extensions

## Accessing the Extension Manager

The Extension Manager is accessible at:

1. `/admin/extensions` - Integrated with the Open WebUI admin interface
2. `/api/_extensions/ui` - Standalone interface

## Installing Extensions

Extensions can be installed via:

1. The Extension Manager UI
   - Click the "Choose File" button in the "Install New Extension" section
   - Select a ZIP file containing the extension
   - Click "Upload Extension"

2. The `openwebui-ext` CLI tool
   ```bash
   openwebui-ext install /path/to/extension

Managing Extensions
Enabling/Disabling Extensions

In the Extension Manager UI, click the "Enable" or "Disable" button for an extension
Via the CLI:
# Enable an extension
openwebui-ext enable extension_id

# Disable an extension
openwebui-ext disable extension_id

Uninstalling Extensions

In the Extension Manager UI, click the "Uninstall" button for an extension
Via the CLI:
openwebui-ext uninstall extension_id

Configuring Extensions

In the Extension Manager UI, click the "Settings" button for an extension
Extension settings are specific to each extension

Extension Directory
Extensions are stored in:

~/.openwebui/extensions - User extensions



The Extension Manager can be extended with additional functionality:

- **Plugin Repository**: Add support for installing extensions from a central repository
- **Extension Verification**: Add support for verifying extension integrity
- **Dependency Management**: Add support for managing extension dependencies
- **Version Management**: Add support for upgrading/downgrading extensions

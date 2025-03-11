# Extension Manager

The Extension Manager provides an admin interface for managing extensions in Open WebUI.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Using the Extension Manager](#using-the-extension-manager)
- [Extension Manager API](#extension-manager-api)
- [Architecture](#architecture)

## Overview

The Extension Manager allows you to:

- View installed extensions
- Enable/disable extensions
- Install new extensions
- Configure extension settings
- Uninstall extensions

## Installation

The Extension Manager can be installed using the provided installation script:

```bash
# Clone the repository
git clone https://github.com/open-webui/extension-manager.git
cd extension-manager

# Run the installer
python install.py
```

The installer will:

1. Install required dependencies
2. Install the extension system as a package
3. Create an extensions directory in your Open WebUI installation
4. Link the Extension Manager to the extensions directory

## Using the Extension Manager

After installation, the Extension Manager will be available in the Admin Settings of Open WebUI.

### Viewing Extensions

The Extension Manager displays a list of all installed extensions. Each extension card shows:

- Extension name and version
- Description
- Author
- Type (UI, API, Model, Tool, Theme)
- Status (Active, Inactive, Error, Pending)
- Installation date and update date

You can filter extensions by:

- Type
- Status
- Source
- Search query

### Installing Extensions

To install a new extension:

1. Click the "Install Extension" button
2. Select the installation source:
   - Remote URL (ZIP file)
   - Local Directory
   - Extension Marketplace (coming soon)
3. Enter the required information for the selected source
4. Click "Install Extension"

### Enabling/Disabling Extensions

To enable an extension, click the "Enable" button on the extension card.

To disable an extension, click the "Disable" button on the extension card.

### Configuring Extensions

To configure an extension:

1. Click the "Settings" button on the extension card
2. Modify the extension settings
3. Click "Save Settings"

### Uninstalling Extensions

To uninstall an extension:

1. Click the "Uninstall" button on the extension card
2. Confirm the uninstallation

## Extension Manager API

The Extension Manager provides a REST API for managing extensions:

### List Extensions

```
GET /api/extensions
```

Query Parameters:
- `types`: Filter by extension types (comma-separated)
- `status`: Filter by extension status (comma-separated)
- `sources`: Filter by extension sources (comma-separated)
- `search`: Search query
- `page`: Page number for pagination
- `page_size`: Number of items per page

### Get Extension

```
GET /api/extensions/{name}
```

Path Parameters:
- `name`: The name of the extension

### Install Extension

```
POST /api/extensions/install
```

Request Body:
```json
{
  "source": "remote", // "remote", "local", or "marketplace"
  "url": "https://example.com/extension.zip", // for remote sources
  "path": "/path/to/extension", // for local sources
  "name": "extension-name" // for marketplace sources
}
```

### Perform Extension Action

```
POST /api/extensions/action
```

Request Body:
```json
{
  "action": "enable", // "enable", "disable", or "uninstall"
  "name": "extension-name"
}
```

### Update Extension Settings

```
POST /api/extensions/settings
```

Request Body:
```json
{
  "name": "extension-name",
  "settings": {
    "setting1": "value1",
    "setting2": "value2"
  }
}
```

### Discover Extensions

```
POST /api/extensions/discover
```

### Initialize Extensions

```
POST /api/extensions/initialize
```

## Architecture

The Extension Manager consists of the following components:

### Backend Components

- **Registry**: Manages the lifecycle of extensions
- **API**: Provides a REST API for managing extensions
- **Models**: Defines data models for extensions

### Frontend Components

- **ExtensionManager**: Main UI component for the Extension Manager
- **ExtensionCard**: UI component for displaying an extension
- **ExtensionForm**: UI component for installing extensions

### Integration with Open WebUI

The Extension Manager integrates with Open WebUI through:

1. **API Integration**: Provides API endpoints for managing extensions
2. **UI Integration**: Adds UI components to the admin settings
3. **Hook System**: Uses hooks to integrate with Open WebUI

### Extensibility

The Extension Manager can be extended with additional functionality:

- **Plugin Repository**: Add support for installing extensions from a central repository
- **Extension Verification**: Add support for verifying extension integrity
- **Dependency Management**: Add support for managing extension dependencies
- **Version Management**: Add support for upgrading/downgrading extensions

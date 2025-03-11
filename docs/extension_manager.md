# Extension Manager Guide

The Extension Manager provides a user-friendly interface for managing extensions in Open WebUI.

## Accessing the Extension Manager

After installation, you can access the Extension Manager through the admin panel:

1. Log in to Open WebUI as an administrator
2. Go to **Admin > Extensions**

## Features

The Extension Manager provides the following features:

### Viewing Installed Extensions

The main page displays all installed extensions with their:

- Name and description
- Version
- Author
- Status (enabled/disabled)
- Tags

### Installing Extensions

To install a new extension:

1. Click the **Install Extension** button
2. Select an extension package (.zip file)
3. Click **Install**

Extension packages should contain a complete extension directory structure.

### Enabling/Disabling Extensions

To enable or disable an extension:

1. Find the extension in the list
2. Toggle the switch next to the extension

Disabled extensions will not be loaded when Open WebUI starts.

### Uninstalling Extensions

To uninstall an extension:

1. Find the extension in the list
2. Click the **Delete** button
3. Confirm the deletion

Note: Uninstalling an extension will remove all its files and configuration.

## Example Extensions

The Extension System includes example extensions:

### MCP Connector

The MCP Connector extension allows connecting to MCP (Model Context Protocol) servers.

To use the MCP Connector:

1. Navigate to **MCP Servers** in the sidebar
2. Click **Add Server** to add a new MCP server
3. Enter the server details:
   - Name: A friendly name for the server
   - URL: The base URL of the MCP server (e.g., http://localhost:11434/v1)
   - API Key: Optional API key for authentication
   - Description: Optional description of the server
4. Click **Save** to add the server
5. Enable the server to make its models available in Open WebUI

### Example Extension

The Example Extension demonstrates basic extension features:

1. Navigate to **Example Extension** in the sidebar
2. Explore the example dashboard
3. Test the API example

## Troubleshooting

### Extension Not Showing Up

If an extension does not appear in the Extension Manager:

1. Check the Open WebUI logs for errors
2. Ensure the extension has a valid `__init__.py` file
3. Restart Open WebUI

### Extension Not Working

If an extension is installed but not working:

1. Check if the extension is enabled
2. Check the Open WebUI logs for errors
3. Ensure the extension is compatible with your version of Open WebUI
4. Check if the extension has any dependencies that need to be installed

### Cannot Install Extension

If you cannot install an extension:

1. Ensure the extension package (.zip) has the correct structure
2. Check if the extension is already installed
3. Ensure you have permission to write to the extensions directory
4. Check the Open WebUI logs for errors

## Extension Settings

Some extensions may provide settings that can be configured through the Extension Manager:

1. Find the extension in the list
2. Click the **Settings** button (if available)
3. Configure the extension settings
4. Click **Save** to apply the settings

## Extension Hooks

Extensions can integrate with various parts of Open WebUI through hooks.

Hooks provide a way for extensions to:

- Modify UI components
- Add custom behavior
- Integrate with other extensions
- Extend core functionality

## Advanced Topics

### Extension Dependencies

Extensions can depend on other extensions. The Extension Manager will ensure that dependencies are installed and enabled before loading an extension.

### Extension Configuration

Extensions can store configuration data in the `config` directory. This data is preserved when the extension is updated.

### Extension Data

Extensions can store data in the `data` directory. This data is preserved when the extension is updated.

### Extension Lifecycle

Extensions go through the following lifecycle:

1. Installation: When the extension is installed
2. Initialization: When the extension is loaded
3. Startup: When the extension is started
4. Shutdown: When the extension is shut down
5. Uninstallation: When the extension is uninstalled

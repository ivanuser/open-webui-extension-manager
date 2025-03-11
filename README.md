# Open WebUI Extension System

The Open WebUI Extension System provides a comprehensive framework for creating, installing, and managing extensions for Open WebUI. This system allows developers to enhance Open WebUI with new features, integrations, and capabilities.

## Key Features

- **Extension Manager**: User-friendly interface for installing, configuring, and managing extensions
- **Extension Framework**: Standardized framework for creating different types of extensions
- **Integrated API**: Seamless integration with Open WebUI's core features
- **MCP Connector**: Example extension for connecting to Model Context Protocol (MCP) servers

## Installation

### Quick Install (Recommended)

```bash
# Install the Extension Manager directly from GitHub
curl -sSL https://raw.githubusercontent.com/open-webui/extensions/main/install.sh | bash
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/open-webui/extensions.git
   cd extensions
   ```

2. Run the installation script:
   ```bash
   python install.py
   ```

3. Restart Open WebUI to apply changes

## Using the Extension Manager

After installation, restart Open WebUI and access the Extension Manager:

1. Log in to Open WebUI
2. Go to Admin > Extensions
3. Use the interface to manage your extensions

## Creating Extensions

See [Creating Extensions](docs/creating_extensions.md) for a detailed guide.

## Documentation

- [Extension Manager Guide](docs/extension_manager.md)
- [Creating Extensions](docs/creating_extensions.md)
- [Extension API Reference](docs/extension_api.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Open WebUI Extension System

A comprehensive extension system for Open WebUI that allows developers to create custom extensions to enhance functionality.

## Features

- **Extension Manager**: Admin interface for managing extensions
- **Extension Framework**: Core libraries and interfaces for extension development
- **Extension Registry**: System for discovering and loading extensions
- **Extension API**: Standard interfaces for extensions to integrate with Open WebUI

## Installation

### Option 1: Automatic Installation

```bash
# Clone the repository
git clone https://github.com/open-webui/extension-manager.git
cd extension-manager

# Run the installer
python install.py
```

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/open-webui/extension-manager.git
cd extension-manager

# Install dependencies
pip install -r requirements.txt

# Install as an editable package
pip install -e .

# Copy or symlink the extension_manager directory to your Open WebUI installation
ln -s $(pwd)/extension_manager /path/to/open-webui/extensions/manager
```

## Usage

After installation, the Extension Manager will be available in the Admin Settings of Open WebUI.

### Managing Extensions

- **View Extensions**: See all installed extensions
- **Enable/Disable**: Toggle extensions on or off
- **Install Extensions**: Add new extensions from various sources
- **Configure Extensions**: Adjust settings for installed extensions
- **Uninstall Extensions**: Remove extensions from the system

## Creating Extensions

See [Creating Extensions](docs/creating_extensions.md) for a detailed guide on how to create your own extensions.

## Extension Types

- **UI Extensions**: Add new UI components
- **API Extensions**: Add new API endpoints
- **Model Adapters**: Integrate new AI models
- **Tool Extensions**: Add new tools or capabilities
- **Theme Extensions**: Customize the appearance

## Documentation

- [Creating Extensions](docs/creating_extensions.md)
- [Extension API](docs/extension_api.md)
- [Extension Manager](docs/extension_manager.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

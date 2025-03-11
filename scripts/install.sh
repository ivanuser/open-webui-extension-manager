#!/bin/bash

# Open WebUI Extension Manager - Installer Script
# This script downloads and runs the Python installer

echo "====================================================="
echo " Open WebUI Extension Manager - Installer"
echo "====================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 could not be found. Please install Python 3 and try again."
    exit 1
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "📁 Created temporary directory: $TEMP_DIR"

# Download the installer
INSTALLER_URL="https://raw.githubusercontent.com/open-webui/extensions/main/install.py"
INSTALLER_PATH="$TEMP_DIR/install.py"

echo "⬇️ Downloading installer from $INSTALLER_URL..."
if command -v curl &> /dev/null
then
    curl -sSL "$INSTALLER_URL" -o "$INSTALLER_PATH"
elif command -v wget &> /dev/null
then
    wget -q "$INSTALLER_URL" -O "$INSTALLER_PATH"
else
    echo "❌ Neither curl nor wget found. Please install one of them and try again."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Make the installer executable
chmod +x "$INSTALLER_PATH"

# Run the installer
echo "🚀 Running installer..."
python3 "$INSTALLER_PATH"

# Clean up
echo "🧹 Cleaning up..."
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Installation process completed."

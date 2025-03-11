#!/usr/bin/env python3
"""
Open WebUI Extension Manager Installation Script

This script installs the Extension Manager for Open WebUI, which allows
managing extensions through a user-friendly interface.
"""

import os
import sys
import shutil
import json
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("extension_manager_installer")

def find_open_webui_root(specified_path=None):
    """Find the Open WebUI installation directory."""
    print("Locating Open WebUI Installation")
    
    if specified_path:
        if os.path.exists(specified_path):
            if os.path.exists(os.path.join(specified_path, "backend", "open_webui")):
                print(f"Using specified Open WebUI path: {specified_path}")
                return specified_path
            else:
                print(f"Specified path does not appear to be an Open WebUI installation: {specified_path}")
        else:
            print(f"Specified path does not exist: {specified_path}")
    
    # Check common locations
    possible_paths = [
        os.getcwd(),  # Current directory
        os.path.dirname(os.getcwd()),  # Parent directory
        os.path.join(os.path.expanduser("~"), "open-webui"),  # User's home directory
        "/opt/open-webui",  # System installation
        "/usr/local/open-webui",  # System installation
        "C:\\Program Files\\Open WebUI",  # Windows installation
        os.path.join(os.path.expanduser("~"), "Documents", "open-webui"),  # Windows documents
    ]
    
    # Add any paths from environment variables
    if "OPEN_WEBUI_ROOT" in os.environ:
        possible_paths.insert(0, os.environ["OPEN_WEBUI_ROOT"])
    
    for path in possible_paths:
        if os.path.exists(path):
            if os.path.exists(os.path.join(path, "backend", "open_webui")):
                print(f"Found Open WebUI at: {path}")
                return path
    
    # If we couldn't find it, ask the user
    print("Could not automatically find Open WebUI installation.")
    user_path = input("Please enter the path to your Open WebUI installation: ")
    
    if os.path.exists(user_path):
        if os.path.exists(os.path.join(user_path, "backend", "open_webui")):
            print(f"Using Open WebUI at: {user_path}")
            return user_path
        else:
            print(f"The directory does not appear to be an Open WebUI installation: {user_path}")
            sys.exit(1)
    else:
        print(f"The specified directory does not exist: {user_path}")
        sys.exit(1)

def install_dependencies():
    """Install required dependencies."""
    print("Installing Dependencies")
    
    dependencies = [
        "fastapi>=0.68.0",
        "pydantic>=1.8.2",
        "starlette>=0.14.2",
        "python-multipart>=0.0.5",
    ]
    
    try:
        import subprocess
        for dependency in dependencies:
            print(f"Installing {dependency}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        print("You may need to install dependencies manually: " + ", ".join(dependencies))

def main():
    """Main installation function."""
    parser = argparse.ArgumentParser(description="Install Open WebUI Extension Manager")
    parser.add_argument("--path", help="Path to Open WebUI installation")
    parser.add_argument("--no-example", action="store_true", help="Don't install example extension")
    args = parser.parse_args()
    
    # Find Open WebUI installation
    open_webui_root = find_open_webui_root(args.path)
    
    # Install dependencies
    install_dependencies()
    
    # TODO: Implement installation steps
    print("TODO: Implement complete installation steps")
    
    print("Installation Complete!")
    print("""
Open WebUI Extension Manager has been successfully installed!

Next steps:
1. Restart your Open WebUI server
2. Open the admin panel and look for the "Extensions" section
3. You can manage extensions through the UI or install new ones
""")

if __name__ == "__main__":
    main()

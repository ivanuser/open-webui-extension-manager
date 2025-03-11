#!/usr/bin/env python3
"""
Open WebUI Extension Manager Installation Script

This script installs the Extension Manager for Open WebUI, which allows
managing extensions through a user-friendly interface.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_requirements():
    try:
        import fastapi
        import pydantic
        import aiofiles
        print("✅ Required dependencies already installed")
    except ImportError:
        print("⚠️ Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_extension_system():
    print("Installing Open WebUI Extension System...")
    
    # Get the Open WebUI installation directory
    webui_dir = input("Enter the path to your Open WebUI installation: ")
    webui_path = Path(webui_dir)
    
    if not webui_path.exists():
        print(f"❌ Error: The path {webui_dir} does not exist")
        return False
    
    # Install the extension system as a package
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    
    # Copy the extension manager to the Open WebUI directory
    ext_manager_path = webui_path / "extensions"
    os.makedirs(ext_manager_path, exist_ok=True)
    
    # Create the extensions directory if it doesn't exist
    extensions_dir = webui_path / "extensions"
    os.makedirs(extensions_dir, exist_ok=True)
    
    # Create a symbolic link to the extension manager in the Open WebUI directory
    ext_manager_src = Path(__file__).parent / "extension_manager"
    if os.name == 'nt':  # Windows
        subprocess.check_call(
            f'mklink /D "{extensions_dir / "manager"}" "{ext_manager_src}"', 
            shell=True
        )
    else:  # Unix-like
        os.symlink(ext_manager_src, extensions_dir / "manager")
    
    print("✅ Extension system installed successfully")
    print(f"The extension manager is now available at {extensions_dir / 'manager'}")
    return True

if __name__ == "__main__":
    check_requirements()
    if install_extension_system():
        print("🚀 Open WebUI Extension System is ready to use!")
        print("To access the Extension Manager, go to Admin Settings in Open WebUI")

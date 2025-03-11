#!/usr/bin/env python3
"""
Integration script for Open WebUI Extension Manager.

This script helps integrate the Extension Manager with an existing Open WebUI installation.
"""

import os
import sys
import shutil
import argparse
import logging
import json
import importlib.util
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("integrate_with_webui")

def find_webui_module():
    """Try to import the Open WebUI module to find its location."""
    try:
        spec = importlib.util.find_spec("openwebui")
        if spec is not None:
            return Path(spec.origin).parent
    except ImportError:
        pass
    
    return None

def find_webui_config():
    """Find the Open WebUI configuration file."""
    config_paths = [
        Path.home() / ".config" / "openwebui" / "config.json",
        Path("/etc/openwebui/config.json"),
        Path("./config.json"),
    ]
    
    for path in config_paths:
        if path.exists():
            return path
    
    return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Integrate Extension Manager with Open WebUI")
    
    parser.add_argument(
        "--webui-dir", 
        help="Path to Open WebUI installation"
    )
    
    parser.add_argument(
        "--extensions-dir", 
        help="Path to extensions directory"
    )
    
    parser.add_argument(
        "--config-file", 
        help="Path to Open WebUI configuration file"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install dependencies"
    )
    
    return parser.parse_args()

def install_dependencies():
    """Install required dependencies."""
    try:
        import subprocess
        
        logger.info("Installing required dependencies...")
        
        # Install from requirements.txt if it exists
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            # Install essential dependencies
            dependencies = [
                "fastapi>=0.68.0",
                "pydantic>=1.8.2",
                "aiofiles>=0.7.0",
                "python-multipart>=0.0.5",
                "PyYAML>=6.0",
            ]
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
        
        logger.info("Dependencies installed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error installing dependencies: {e}")
        return False

def integrate_with_webui(webui_dir, extensions_dir=None, config_file=None):
    """Integrate the Extension Manager with Open WebUI.
    
    Args:
        webui_dir: Path to Open WebUI installation.
        extensions_dir: Path to extensions directory.
        config_file: Path to Open WebUI configuration file.
    
    Returns:
        True if integration was successful, False otherwise.
    """
    try:
        webui_path = Path(webui_dir)
        
        # Verify Open WebUI directory
        if not webui_path.exists():
            logger.error(f"Open WebUI directory {webui_dir} does not exist.")
            return False
        
        # Determine extensions directory
        if not extensions_dir:
            extensions_dir = webui_path / "extensions"
        else:
            extensions_dir = Path(extensions_dir)
        
        # Create extensions directory if it doesn't exist
        extensions_dir.mkdir(exist_ok=True)
        
        # Copy extension_manager to extensions directory
        extension_manager_src = Path(__file__).parent / "extension_manager"
        extension_manager_dst = extensions_dir / "manager"
        
        if extension_manager_dst.exists():
            logger.warning(f"Extension Manager already exists at {extension_manager_dst}. Removing.")
            shutil.rmtree(extension_manager_dst)
        
        logger.info(f"Copying Extension Manager to {extension_manager_dst}")
        shutil.copytree(extension_manager_src, extension_manager_dst)
        
        # Copy extension_framework to Open WebUI site-packages
        try:
            import site
            site_packages = Path(site.getsitepackages()[0])
            
            extension_framework_src = Path(__file__).parent / "extension_framework"
            extension_framework_dst = site_packages / "extension_framework"
            
            if extension_framework_dst.exists():
                logger.warning(f"Extension Framework already exists at {extension_framework_dst}. Removing.")
                shutil.rmtree(extension_framework_dst)
            
            logger.info(f"Copying Extension Framework to {extension_framework_dst}")
            shutil.copytree(extension_framework_src, extension_framework_dst)
        except Exception as e:
            logger.error(f"Error copying Extension Framework: {e}")
            logger.warning("You may need to manually install the Extension Framework package.")
        
        # Copy example extension to extensions directory
        example_extension_src = Path(__file__).parent / "example_extension"
        example_extension_dst = extensions_dir / "example_extension"
        
        if example_extension_dst.exists():
            logger.warning(f"Example Extension already exists at {example_extension_dst}. Skipping.")
        else:
            logger.info(f"Copying Example Extension to {example_extension_dst}")
            shutil.copytree(example_extension_src, example_extension_dst)
        
        # Update Open WebUI configuration
        if config_file:
            update_webui_config(config_file, extensions_dir)
        
        logger.info("Integration completed successfully!")
        logger.info("To use the Extension Manager, restart Open WebUI and go to Admin Settings.")
        
        return True
    except Exception as e:
        logger.error(f"Error integrating with Open WebUI: {e}")
        return False

def update_webui_config(config_file, extensions_dir):
    """Update Open WebUI configuration to enable extensions.
    
    Args:
        config_file: Path to Open WebUI configuration file.
        extensions_dir: Path to extensions directory.
    """
    try:
        config_path = Path(config_file)
        
        if not config_path.exists():
            logger.warning(f"Configuration file {config_file} does not exist. Skipping configuration update.")
            return
        
        # Read existing configuration
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Update configuration
        if "extensions" not in config:
            config["extensions"] = {}
        
        config["extensions"]["enabled"] = True
        config["extensions"]["directory"] = str(extensions_dir)
        
        # Write updated configuration
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Updated Open WebUI configuration at {config_file}")
    except Exception as e:
        logger.error(f"Error updating Open WebUI configuration: {e}")
        logger.warning("You may need to manually update the configuration to enable extensions.")

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            logger.error("Failed to install dependencies. Aborting.")
            return 1
    
    # Find Open WebUI installation
    webui_dir = args.webui_dir
    if not webui_dir:
        webui_module = find_webui_module()
        if webui_module:
            webui_dir = webui_module.parent
            logger.info(f"Found Open WebUI at {webui_dir}")
        else:
            webui_dir = input("Enter the path to your Open WebUI installation: ")
    
    # Find configuration file
    config_file = args.config_file
    if not config_file:
        config_file = find_webui_config()
        if config_file:
            logger.info(f"Found Open WebUI configuration at {config_file}")
    
    # Integrate with Open WebUI
    if not integrate_with_webui(webui_dir, args.extensions_dir, config_file):
        logger.error("Integration failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

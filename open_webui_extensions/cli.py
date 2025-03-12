import click
import os
import sys
import logging
import asyncio
from pathlib import Path

from .extension_system.registry import extension_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

@click.group()
def cli():
    """Open WebUI Extension Manager CLI."""
    pass

@cli.command()
def setup():
    """Set up the extension system."""
    # Ensure extension directories exist
    for ext_dir in extension_registry.extension_dirs:
        os.makedirs(ext_dir, exist_ok=True)
        logger.info(f"Extension directory created: {ext_dir}")
    
    logger.info("Extension system set up successfully.")

@cli.command()
def list():
    """List all installed extensions."""
    extensions = extension_registry.get_all_extensions()
    
    if not extensions:
        logger.info("No extensions installed.")
        return
    
    logger.info(f"Found {len(extensions)} extensions:")
    
    for ext_id, extension in extensions.items():
        status = "Enabled" if extension.enabled else "Disabled"
        name = getattr(extension, "name", ext_id)
        version = getattr(extension, "version", "0.0.0")
        
        logger.info(f"- {name} (v{version}) [{status}]")
        logger.info(f"  ID: {ext_id}")
        
        if hasattr(extension, "description") and extension.description:
            logger.info(f"  Description: {extension.description}")
        
        if hasattr(extension, "author") and extension.author:
            logger.info(f"  Author: {extension.author}")
        
        logger.info("")

@cli.command()
@click.argument("extension_path")
@click.option("--id", help="Extension ID (defaults to directory name)")
def install(extension_path, id=None):
    """Install an extension from a directory."""
    # Ensure the path exists
    if not os.path.exists(extension_path):
        logger.error(f"Path does not exist: {extension_path}")
        sys.exit(1)
    
    # Install the extension
    result = extension_registry.install_extension(extension_path, id)
    
    if result:
        logger.info(f"Extension {result} installed successfully.")
    else:
        logger.error("Failed to install extension.")
        sys.exit(1)

@cli.command()
@click.argument("extension_id")
def uninstall(extension_id):
    """Uninstall an extension."""
    # Uninstall the extension
    success = extension_registry.uninstall_extension(extension_id)
    
    if success:
        logger.info(f"Extension {extension_id} uninstalled successfully.")
    else:
        logger.error(f"Failed to uninstall extension {extension_id}.")
        sys.exit(1)

@cli.command()
@click.argument("extension_id")
def enable(extension_id):
    """Enable an extension."""
    # Enable the extension
    success = extension_registry.enable_extension(extension_id)
    
    if success:
        logger.info(f"Extension {extension_id} enabled successfully.")
    else:
        logger.error(f"Failed to enable extension {extension_id}.")
        sys.exit(1)

@cli.command()
@click.argument("extension_id")
def disable(extension_id):
    """Disable an extension."""
    # Disable the extension
    success = extension_registry.disable_extension(extension_id)
    
    if success:
        logger.info(f"Extension {extension_id} disabled successfully.")
    else:
        logger.error(f"Failed to disable extension {extension_id}.")
        sys.exit(1)

@cli.command()
def dev_server():
    """Run the development server for testing extensions."""
    from .dev_server import run_dev_server
    
    # Run the development server
    run_dev_server()

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()

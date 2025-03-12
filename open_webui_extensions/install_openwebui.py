import os
import shutil
import logging
import argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

def install_admin_integration(open_webui_path=None):
    """Install the admin integration into Open WebUI."""
    if not open_webui_path:
        # Try to find Open WebUI installation
        possible_paths = [
            "/app/backend/app",  # Docker path
            os.path.expanduser("~/open-webui/backend/app"),  # Home directory
            "/usr/local/lib/python3.9/site-packages/app",  # Pip installation
            os.path.expanduser("~/Documents/src/open-webui/backend/app"),  # Windows home
            os.path.expanduser("~/Documents/src/open-webui"),  # Windows direct
            "C:/Users/ihoner/Documents/src/open-webui",  # Specific Windows path
            "C:/Users/ihoner/Documents/src/open-webui/backend/app",  # Specific Windows app path
            os.getcwd(),  # Current directory
            os.path.join(os.getcwd(), "open-webui"),  # Subfolder in current directory
            # Add more possible paths
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found potential Open WebUI path: {path}")
                open_webui_path = path
                break
        
        if not open_webui_path:
            logger.error("Could not find Open WebUI installation. Please specify the path using --path argument.")
            logger.error("Example: python -m open_webui_extensions.install_openwebui --path /path/to/open-webui")
            return False
    
    logger.info(f"Using Open WebUI path: {open_webui_path}")
    
    # Check if this is a valid Open WebUI installation
    admin_path = os.path.join(open_webui_path, "backend", "app", "frontend", "src", "routes", "admin")
    if not os.path.exists(admin_path):
        # Try alternative structure (maybe the path is already pointing to backend/app)
        admin_path = os.path.join(open_webui_path, "frontend", "src", "routes", "admin")
        if not os.path.exists(admin_path):
            logger.error(f"Admin interface not found at {admin_path}")
            logger.error("The specified path does not appear to be a valid Open WebUI installation.")
            logger.error("Please ensure you're pointing to the root of the Open WebUI repository.")
            return False
    
    # Path to admin layout
    layout_file = os.path.join(admin_path, "+layout.svelte")
    if not os.path.exists(layout_file):
        logger.error(f"Admin layout not found at {layout_file}")
        return False
    
    # Add our extension script to the admin layout
    try:
        # Read the layout file
        with open(layout_file, "r") as f:
            content = f.read()
        
        # Check if our integration is already added
        if '<script src="/api/_extensions/ui/admin-integration.js"></script>' in content:
            logger.info("Admin integration already installed.")
            return True
        
        # Add our script to the layout
        # Insert before the closing </head> tag
        if "</head>" in content:
            content = content.replace(
                "</head>",
                '<script src="/api/_extensions/ui/admin-integration.js"></script>\n</head>'
            )
            
            # Write the modified layout
            with open(layout_file, "w") as f:
                f.write(content)
            
            logger.info("Admin integration installed successfully.")
            return True
        else:
            logger.error("Could not find </head> in admin layout.")
            return False
    
    except Exception as e:
        logger.error(f"Error installing admin integration: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Open WebUI Extension Manager integration')
    parser.add_argument('--path', type=str, help='Path to Open WebUI installation')
    args = parser.parse_args()
    
    install_admin_integration(args.path)

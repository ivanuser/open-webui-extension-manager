import os
import logging
import argparse
import sys
import json
import shutil
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

def install_admin_integration(open_webui_path=None):
    """Install the admin UI integration into Open WebUI."""
    if not open_webui_path:
        # Try to find Open WebUI installation
        possible_paths = [
            # Specific user path provided
            "/home/ihoner/ai_dev/venv/lib/python3.11/site-packages/open_webui",
            "/home/ihoner/ai_dev/openwebui/lib/python3.11/site-packages/open_webui",
            
            # General pip installation paths
            os.path.join(sys.prefix, "lib", "python" + sys.version[:3], "site-packages", "open_webui"),
            os.path.join(os.path.dirname(os.__file__), "site-packages", "open_webui"),
            
            # Docker path
            "/app/backend/app",
            
            # Git clone paths
            os.path.expanduser("~/open-webui/backend/app"),
            os.path.expanduser("~/Documents/src/open-webui"),
            "C:/Users/ihoner/Documents/src/open-webui",
            os.getcwd(),
            os.path.join(os.getcwd(), "open-webui"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found potential Open WebUI path: {path}")
                open_webui_path = path
                break
        
        if not open_webui_path:
            logger.error("Could not find Open WebUI installation. Please specify the path using --path argument.")
            return False
    
    logger.info(f"Using Open WebUI path: {open_webui_path}")
    
    # Find the frontend directory
    frontend_dir = os.path.join(open_webui_path, "frontend")
    if not os.path.exists(frontend_dir):
        logger.error(f"Frontend directory not found at {frontend_dir}")
        return False
    
    # Look for the JS assets directory
    assets_dir = os.path.join(frontend_dir, "assets")
    if not os.path.exists(assets_dir):
        logger.error(f"Assets directory not found at {assets_dir}")
        return False
    
    # Look for the JavaScript files in the assets directory
    js_files = []
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".js"):
                js_files.append(os.path.join(root, file))
    
    logger.info(f"Found {len(js_files)} JavaScript files")
    
    # Create a small JavaScript file that we'll inject
    extensions_js = """
// Extension Manager Sidebar Integration
(function() {
    function waitForSidebar() {
        const sidebar = document.querySelector('.settings-sidebar, .admin-sidebar');
        if (!sidebar) {
            setTimeout(waitForSidebar, 500);
            return;
        }
        
        // Check if our item already exists
        if (document.querySelector('[data-target="extensions"]')) {
            return;
        }
        
        // Create the Extensions menu item
        const extensionsItem = document.createElement('a');
        extensionsItem.href = '#';
        extensionsItem.setAttribute('data-target', 'extensions');
        extensionsItem.className = 'flex items-center p-2 text-gray-500 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 group';
        
        extensionsItem.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-gray-500 dark:text-gray-400 transition duration-75 group-hover:text-gray-900 dark:group-hover:text-white">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
            </svg>
            <span class="ml-3">Extensions</span>
        `;
        
        // Add to sidebar
        sidebar.appendChild(extensionsItem);
        
        // Handle click event
        extensionsItem.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create iframe to load extension manager
            const contentArea = document.querySelector('.content-area, .admin-content-area');
            if (contentArea) {
                // Hide other content
                const otherContent = contentArea.querySelectorAll(':scope > *:not(#extensions-iframe-container)');
                otherContent.forEach(el => {
                    el.style.display = 'none';
                });
                
                // Show extensions iframe
                let iframe = document.getElementById('extensions-iframe');
                let container = document.getElementById('extensions-iframe-container');
                
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'extensions-iframe-container';
                    container.style.width = '100%';
                    container.style.height = '100%';
                    contentArea.appendChild(container);
                    
                    iframe = document.createElement('iframe');
                    iframe.id = 'extensions-iframe';
                    iframe.src = '/extensions/manager';
                    iframe.style.width = '100%';
                    iframe.style.height = '90vh';
                    iframe.style.border = 'none';
                    iframe.style.overflow = 'auto';
                    container.appendChild(iframe);
                } else {
                    container.style.display = 'block';
                }
                
                // Update active state in sidebar
                const activeItem = sidebar.querySelector('.active, .bg-gray-200, .dark\\:bg-gray-700');
                if (activeItem) {
                    activeItem.classList.remove('active', 'bg-gray-200', 'dark:bg-gray-700');
                }
                extensionsItem.classList.add('active', 'bg-gray-200', 'dark:bg-gray-700');
            }
        });
    }
    
    // Check if we're on a settings page
    if (window.location.pathname.includes('/settings') || 
        window.location.pathname.includes('/admin')) {
        // Wait for the page to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', waitForSidebar);
        } else {
            waitForSidebar();
        }
    }
})();
"""
    
    # Create the extensions.js file
    extensions_js_path = os.path.join(frontend_dir, "static", "extensions.js")
    os.makedirs(os.path.dirname(extensions_js_path), exist_ok=True)
    
    with open(extensions_js_path, "w") as f:
        f.write(extensions_js)
    
    logger.info(f"Created extensions.js at {extensions_js_path}")
    
    # Find and modify the main index.html to load our script
    index_html_path = os.path.join(frontend_dir, "index.html")
    if not os.path.exists(index_html_path):
        logger.warning(f"index.html not found at {index_html_path}")
        # Try to find index.html
        for root, dirs, files in os.walk(frontend_dir):
            if "index.html" in files:
                index_html_path = os.path.join(root, "index.html")
                logger.info(f"Found index.html at {index_html_path}")
                break
    
    if os.path.exists(index_html_path):
        with open(index_html_path, "r") as f:
            index_html = f.read()
        
        # Check if our script is already included
        if 'src="/static/extensions.js"' not in index_html:
            # Add our script before the closing </body> tag
            modified_html = index_html.replace(
                '</body>',
                '<script src="/static/extensions.js"></script>\n</body>'
            )
            
            with open(index_html_path, "w") as f:
                f.write(modified_html)
            
            logger.info(f"Added extensions.js to {index_html_path}")
        else:
            logger.info("extensions.js already included in index.html")
    else:
        logger.warning("Could not find index.html, will try to inject into JavaScript files")
        
        # Try to inject our code into the bundled JavaScript files
        modified_any = False
        for js_file in js_files:
            with open(js_file, "r", encoding="utf-8", errors="ignore") as f:
                js_content = f.read()
            
            # Look for initialization code or main component
            if "document.addEventListener" in js_content and "DOMContentLoaded" in js_content:
                # Add our code to the file
                with open(js_file, "a") as f:
                    f.write("\n\n" + extensions_js)
                
                logger.info(f"Injected extensions.js into {js_file}")
                modified_any = True
                break
        
        if not modified_any:
            logger.warning("Could not find suitable JavaScript file to inject code")
            logger.info("You'll need to manually include extensions.js in the frontend")
    
    logger.info("UI integration completed!")
    logger.info("You should now see an 'Extensions' item in the settings sidebar after restarting Open WebUI")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Open WebUI Extension Manager UI integration')
    parser.add_argument('--path', type=str, help='Path to Open WebUI installation')
    args = parser.parse_args()
    
    install_admin_integration(args.path)

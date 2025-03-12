import os
import logging
import argparse
import sys
import json
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

def find_admin_files(base_path):
    """Search recursively for admin-related files."""
    admin_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if "+layout.svelte" in file and "admin" in root.lower():
                admin_files.append(os.path.join(root, file))
    return admin_files

def install_admin_integration(open_webui_path=None):
    """Install the admin integration into Open WebUI."""
    if not open_webui_path:
        # Try to find Open WebUI installation
        possible_paths = [
            # Specific user path provided
            "/home/ihoner/ai_dev/venv/lib/python3.11/site-packages/open_webui",
            
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
    
    # For pip-installed version, we'll create an alternative approach
    # We'll create our extension UI page that can be accessed directly
    
    frontend_dir = os.path.join(open_webui_path, "frontend")
    routers_dir = os.path.join(open_webui_path, "routers")
    
    # Check if the directories exist
    if not os.path.exists(frontend_dir):
        logger.error(f"Frontend directory not found at {frontend_dir}")
        return False
    
    if not os.path.exists(routers_dir):
        logger.error(f"Routers directory not found at {routers_dir}")
        return False
    
    # Create new route for extension manager
    try:
        # List contents of the frontend directory
        logger.info(f"Contents of frontend directory: {', '.join(os.listdir(frontend_dir))}")
        
        # Create a simple HTML file for the extension manager UI
        static_dir = os.path.join(open_webui_path, "static", "extensions")
        os.makedirs(static_dir, exist_ok=True)
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extension Manager</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            margin-top: 0;
        }
        .extension-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .extension-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        .extension-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .extension-title {
            margin: 0;
            font-size: 18px;
            font-weight: 600;
        }
        .extension-version {
            font-size: 12px;
            color: #666;
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .extension-author {
            font-size: 14px;
            color: #666;
            margin: 5px 0;
        }
        .extension-description {
            margin: 10px 0;
            font-size: 14px;
            color: #555;
        }
        .extension-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 15px;
        }
        button {
            padding: 8px 12px;
            border: none;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        .btn-enable {
            background-color: #4CAF50;
            color: white;
        }
        .btn-enable:hover {
            background-color: #3e8e41;
        }
        .btn-disable {
            background-color: #f44336;
            color: white;
        }
        .btn-disable:hover {
            background-color: #d32f2f;
        }
        .btn-uninstall {
            background-color: #f44336;
            color: white;
        }
        .btn-uninstall:hover {
            background-color: #d32f2f;
        }
        .btn-settings {
            background-color: #2196F3;
            color: white;
        }
        .btn-settings:hover {
            background-color: #0b7dda;
        }
        .upload-section {
            margin-top: 30px;
            padding: 20px;
            border: 2px dashed #ddd;
            border-radius: 8px;
            text-align: center;
        }
        .file-input {
            display: none;
        }
        .file-label {
            display: inline-block;
            padding: 10px 20px;
            background-color: #2196F3;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .file-label:hover {
            background-color: #0b7dda;
        }
        .loader {
            border: 3px solid #f3f3f3;
            border-radius: 50%;
            border-top: 3px solid #3498db;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .hidden {
            display: none;
        }
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #333;
            color: white;
            padding: 15px 25px;
            border-radius: 4px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
        }
        .toast.show {
            opacity: 1;
        }
        .toast.success {
            background-color: #4CAF50;
        }
        .toast.error {
            background-color: #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Extension Manager</h1>
        
        <div id="extensions-container" class="extension-grid">
            <!-- Extensions will be loaded here -->
            <div class="loader"></div>
        </div>
        
        <div class="upload-section">
            <h2>Install New Extension</h2>
            <p>Upload a ZIP file containing the extension.</p>
            <label for="extension-file" class="file-label">Choose File</label>
            <input type="file" id="extension-file" class="file-input" accept=".zip">
            <div id="file-name">No file chosen</div>
            <button id="upload-btn" class="btn-enable" disabled>Upload Extension</button>
            <div id="upload-loader" class="loader hidden"></div>
        </div>
    </div>
    
    <div id="toast" class="toast"></div>
    
    <script>
        // DOM Elements
        const extensionsContainer = document.getElementById('extensions-container');
        const fileInput = document.getElementById('extension-file');
        const fileName = document.getElementById('file-name');
        const uploadBtn = document.getElementById('upload-btn');
        const uploadLoader = document.getElementById('upload-loader');
        const toast = document.getElementById('toast');
        
        // Show toast message
        function showToast(message, type = '') {
            toast.textContent = message;
            toast.className = 'toast show ' + type;
            setTimeout(() => {
                toast.className = 'toast';
            }, 3000);
        }
        
        // Load extensions
        async function loadExtensions() {
            try {
                const response = await fetch('/api/extensions/');
                const extensions = await response.json();
                
                extensionsContainer.innerHTML = '';
                
                if (extensions.length === 0) {
                    extensionsContainer.innerHTML = '<p>No extensions installed.</p>';
                    return;
                }
                
                extensions.forEach(extension => {
                    const card = document.createElement('div');
                    card.className = 'extension-card';
                    card.innerHTML = `
                        <div class="extension-header">
                            <h3 class="extension-title">${extension.name || extension.id}</h3>
                            <span class="extension-version">v${extension.version || '0.0.0'}</span>
                        </div>
                        <div class="extension-author">by ${extension.author || 'Unknown'}</div>
                        <div class="extension-description">${extension.description || 'No description available.'}</div>
                        <div class="extension-actions">
                            ${extension.enabled ? 
                                `<button class="btn-disable" data-id="${extension.id}">Disable</button>` : 
                                `<button class="btn-enable" data-id="${extension.id}">Enable</button>`}
                            <button class="btn-settings" data-id="${extension.id}">Settings</button>
                            <button class="btn-uninstall" data-id="${extension.id}">Uninstall</button>
                        </div>
                    `;
                    extensionsContainer.appendChild(card);
                });
                
                // Add event listeners
                document.querySelectorAll('.btn-enable').forEach(btn => {
                    btn.addEventListener('click', enableExtension);
                });
                
                document.querySelectorAll('.btn-disable').forEach(btn => {
                    btn.addEventListener('click', disableExtension);
                });
                
                document.querySelectorAll('.btn-uninstall').forEach(btn => {
                    btn.addEventListener('click', uninstallExtension);
                });
                
                document.querySelectorAll('.btn-settings').forEach(btn => {
                    btn.addEventListener('click', openSettings);
                });
                
            } catch (error) {
                console.error('Error loading extensions:', error);
                extensionsContainer.innerHTML = `<p>Error loading extensions: ${error.message}</p>`;
            }
        }
        
        // Enable extension
        async function enableExtension(event) {
            const extensionId = event.target.getAttribute('data-id');
            try {
                event.target.disabled = true;
                event.target.innerHTML = '<span class="loader"></span> Enabling...';
                
                const response = await fetch(`/api/extensions/${extensionId}/enable`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    showToast(`Extension ${extensionId} enabled successfully.`, 'success');
                    loadExtensions();
                } else {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to enable extension');
                }
            } catch (error) {
                console.error('Error enabling extension:', error);
                showToast(`Error enabling extension: ${error.message}`, 'error');
                event.target.disabled = false;
                event.target.textContent = 'Enable';
            }
        }
        
        // Disable extension
        async function disableExtension(event) {
            const extensionId = event.target.getAttribute('data-id');
            try {
                event.target.disabled = true;
                event.target.innerHTML = '<span class="loader"></span> Disabling...';
                
                const response = await fetch(`/api/extensions/${extensionId}/disable`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    showToast(`Extension ${extensionId} disabled successfully.`, 'success');
                    loadExtensions();
                } else {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to disable extension');
                }
            } catch (error) {
                console.error('Error disabling extension:', error);
                showToast(`Error disabling extension: ${error.message}`, 'error');
                event.target.disabled = false;
                event.target.textContent = 'Disable';
            }
        }
        
        // Uninstall extension
        async function uninstallExtension(event) {
            const extensionId = event.target.getAttribute('data-id');
            
            if (!confirm(`Are you sure you want to uninstall the extension "${extensionId}"?`)) {
                return;
            }
            
            try {
                event.target.disabled = true;
                event.target.innerHTML = '<span class="loader"></span> Uninstalling...';
                
                const response = await fetch(`/api/extensions/${extensionId}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    showToast(`Extension ${extensionId} uninstalled successfully.`, 'success');
                    loadExtensions();
                } else {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to uninstall extension');
                }
            } catch (error) {
                console.error('Error uninstalling extension:', error);
                showToast(`Error uninstalling extension: ${error.message}`, 'error');
                event.target.disabled = false;
                event.target.textContent = 'Uninstall';
            }
        }
        
        // Open settings
        function openSettings(event) {
            const extensionId = event.target.getAttribute('data-id');
            // Placeholder for now - would open a modal or navigate to settings page
            alert(`Settings for ${extensionId} would open here.`);
        }
        
        // Handle file selection
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                fileName.textContent = fileInput.files[0].name;
                uploadBtn.disabled = false;
            } else {
                fileName.textContent = 'No file chosen';
                uploadBtn.disabled = true;
            }
        });
        
        // Upload extension
        uploadBtn.addEventListener('click', async () => {
            if (!fileInput.files.length) return;
            
            const file = fileInput.files[0];
            if (!file.name.endsWith('.zip')) {
                showToast('Please select a valid ZIP file.', 'error');
                return;
            }
            
            try {
                uploadBtn.disabled = true;
                uploadLoader.classList.remove('hidden');
                
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch('/api/extensions/install', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    showToast(`Extension ${data.extension_id} installed successfully.`, 'success');
                    loadExtensions();
                    
                    // Reset form
                    fileInput.value = '';
                    fileName.textContent = 'No file chosen';
                } else {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to install extension');
                }
            } catch (error) {
                console.error('Error installing extension:', error);
                showToast(`Error installing extension: ${error.message}`, 'error');
            } finally {
                uploadBtn.disabled = false;
                uploadLoader.classList.add('hidden');
            }
        });
        
        // Initialize
        document.addEventListener('DOMContentLoaded', loadExtensions);
    </script>
</body>
</html>
        """
        
        html_path = os.path.join(static_dir, "manager.html")
        with open(html_path, "w") as f:
            f.write(html_content)
        
        # Create a new router file for extensions
        # Make sure we don't use triple quotes inside triple quotes (which caused the syntax error)
        ext_router_content = '''from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from typing import List, Dict, Any, Optional
import os
import sys
import logging
import importlib.util
from pathlib import Path

# Create router
router = APIRouter()

@router.get("/manager", response_class=HTMLResponse)
async def extension_manager():
    # Return the extension manager UI
    html_path = Path(__file__).parent / "../static/extensions/manager.html"
    if not html_path.exists():
        return HTMLResponse(content="<h1>Extension Manager UI not found</h1>")
    
    with open(html_path, "r") as f:
        return HTMLResponse(content=f.read())

@router.get("/")
async def list_extensions():
    # Placeholder - to be implemented with the actual extension system
    return []

# Add more API endpoints for extension management here
'''
        
        ext_router_path = os.path.join(routers_dir, "extensions.py")
        with open(ext_router_path, "w") as f:
            f.write(ext_router_content)
        
        # Now, modify the main.py file to include our router
        main_py_path = os.path.join(open_webui_path, "main.py")
        
        if not os.path.exists(main_py_path):
            logger.error(f"main.py not found at {main_py_path}")
            return False
        
        with open(main_py_path, "r") as f:
            main_content = f.read()
        
        # Check if our router is already included
        if "from routers import extensions" not in main_content:
            # Add import
            import_line = "from fastapi import FastAPI"
            modified_import = "from fastapi import FastAPI\nfrom routers import extensions"
            main_content = main_content.replace(import_line, modified_import)
            
            # Add router inclusion - look for other app.include_router lines and add ours after
            include_router_line = "app.include_router(routers.chat.router)"
            if include_router_line in main_content:
                modified_router_line = f"{include_router_line}\napp.include_router(extensions.router, prefix='/api/extensions', tags=['extensions'])"
                main_content = main_content.replace(include_router_line, modified_router_line)
            else:
                # If the specific line isn't found, try to add before server startup
                startup_line = "@app.on_event(\"startup\")"
                if startup_line in main_content:
                    modified_startup = f"app.include_router(extensions.router, prefix='/api/extensions', tags=['extensions'])\n\n{startup_line}"
                    main_content = main_content.replace(startup_line, modified_startup)
                else:
                    logger.warning("Could not find a good place to insert the router in main.py")
                    logger.warning("You'll need to manually add: app.include_router(extensions.router, prefix='/api/extensions', tags=['extensions'])")
            
            # Write modified content back
            with open(main_py_path, "w") as f:
                f.write(main_content)
            
            logger.info("Added extensions router to main.py")
        else:
            logger.info("Extensions router already included in main.py")
        
        logger.info("Extension manager integration successful!")
        logger.info("Access the extension manager at: /api/extensions/manager")
        
        return True
    
    except Exception as e:
        logger.error(f"Error setting up extension manager: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Open WebUI Extension Manager integration')
    parser.add_argument('--path', type=str, help='Path to Open WebUI installation')
    args = parser.parse_args()
    
    install_admin_integration(args.path)

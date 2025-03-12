import os
import logging
import argparse
import sys
import json
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

def install_admin_integration(open_webui_path=None):
    """Install the admin integration into Open WebUI."""
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
    
    # Create our extension directory and files
    try:
        # Create necessary directories
        static_dir = os.path.join(open_webui_path, "static", "extensions")
        os.makedirs(static_dir, exist_ok=True)
        
        extensions_dir = os.path.join(os.path.expanduser("~"), ".openwebui", "extensions")
        os.makedirs(extensions_dir, exist_ok=True)
        
        # Create the HTML manager page
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
                const response = await fetch('/extensions/api/list');
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
                
                const response = await fetch(`/extensions/api/${extensionId}/enable`, {
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
                
                const response = await fetch(`/extensions/api/${extensionId}/disable`, {
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
                
                const response = await fetch(`/extensions/api/${extensionId}/uninstall`, {
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
                
                const response = await fetch('/extensions/api/install', {
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
        logger.info(f"Created extension manager UI at {html_path}")
        
        # Create direct route implementation file
        extensions_py_content = '''
# Extension system implementation
import os
import sys
import importlib
import importlib.util
import json
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

# Extension base class definition
class Extension:
    """Base class for all extensions."""
    
    # Extension metadata
    id: str = None
    name: str = None
    description: str = None
    version: str = None
    author: str = None
    
    # Extension state
    enabled: bool = False
    installed: bool = False
    path: str = None
    
    def __init__(self):
        if not self.id:
            self.id = self.__class__.__module__
    
    async def startup(self) -> None:
        """Called when the extension is started."""
        pass
    
    async def shutdown(self) -> None:
        """Called when the extension is stopped."""
        pass

# Registry for managing extensions
class ExtensionRegistry:
    """Registry for discovering and loading extensions."""
    
    _instance = None
    extensions: Dict[str, Extension] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExtensionRegistry, cls).__new__(cls)
            cls._instance.extensions = {}
            
            # Set up extension directory
            home_dir = os.path.expanduser("~")
            cls._instance.extension_dir = os.path.join(home_dir, ".openwebui", "extensions")
            os.makedirs(cls._instance.extension_dir, exist_ok=True)
        
        return cls._instance
    
    def discover_extensions(self) -> List[str]:
        """Discover all available extensions."""
        extension_ids = []
        
        # Check the extension directory
        if not os.path.exists(self.extension_dir):
            return extension_ids
        
        # Look for extension packages
        for item in os.listdir(self.extension_dir):
            item_path = os.path.join(self.extension_dir, item)
            
            # Skip non-directories
            if not os.path.isdir(item_path):
                continue
            
            # Check if it's a Python package
            init_file = os.path.join(item_path, "__init__.py")
            if os.path.exists(init_file):
                extension_ids.append(item)
        
        return extension_ids
    
    def load_extension(self, extension_id: str) -> Optional[Extension]:
        """Load an extension by ID."""
        if extension_id in self.extensions:
            return self.extensions[extension_id]
        
        # Check if the extension exists
        ext_path = os.path.join(self.extension_dir, extension_id)
        if not os.path.exists(ext_path):
            return None
        
        # Add to Python path if not already there
        if ext_path not in sys.path:
            sys.path.insert(0, ext_path)
        
        try:
            # Import the module
            spec = importlib.util.find_spec(extension_id)
            if spec is None:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find extension class
            extension_class = None
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and issubclass(obj, Extension) and obj is not Extension:
                    extension_class = obj
                    break
            
            if extension_class:
                extension = extension_class()
                extension.id = extension_id
                extension.installed = True
                extension.path = ext_path
                
                # Load enabled state
                extension.enabled = self._get_extension_state(extension_id)
                
                self.extensions[extension_id] = extension
                return extension
            
        except Exception as e:
            print(f"Error loading extension {extension_id}: {str(e)}")
        
        return None
    
    def get_all_extensions(self) -> Dict[str, Extension]:
        """Get all loaded extensions."""
        # Discover and load any new extensions
        for extension_id in self.discover_extensions():
            if extension_id not in self.extensions:
                self.load_extension(extension_id)
        
        return self.extensions
    
    def enable_extension(self, extension_id: str) -> bool:
        """Enable an extension."""
        extension = self.load_extension(extension_id)
        if not extension:
            return False
        
        extension.enabled = True
        
        # Save enabled state
        self._save_extension_state(extension_id, True)
        
        return True
    
    def disable_extension(self, extension_id: str) -> bool:
        """Disable an extension."""
        extension = self.load_extension(extension_id)
        if not extension:
            return False
        
        extension.enabled = False
        
        # Save enabled state
        self._save_extension_state(extension_id, False)
        
        return True
    
    def install_extension(self, zip_path: str) -> Optional[str]:
        """Install an extension from a ZIP file."""
        try:
            # Extract to a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract the ZIP file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the extension directory (containing __init__.py)
                extension_dir = None
                for root, dirs, files in os.walk(temp_dir):
                    if "__init__.py" in files:
                        extension_dir = root
                        break
                
                if not extension_dir:
                    return None
                
                # Get the extension ID from the directory name
                extension_id = os.path.basename(extension_dir)
                
                # Destination directory
                dest_dir = os.path.join(self.extension_dir, extension_id)
                
                # Remove existing extension if it exists
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                
                # Copy extension files
                shutil.copytree(extension_dir, dest_dir)
                
                # Load the extension
                extension = self.load_extension(extension_id)
                if extension:
                    return extension_id
        
        except Exception as e:
            print(f"Error installing extension: {str(e)}")
        
        return None
    
    def uninstall_extension(self, extension_id: str) -> bool:
        """Uninstall an extension."""
        extension = self.load_extension(extension_id)
        if not extension:
            return False
        
        # Disable the extension first
        self.disable_extension(extension_id)
        
        # Remove the extension directory
        ext_path = os.path.join(self.extension_dir, extension_id)
        if os.path.exists(ext_path):
            shutil.rmtree(ext_path)
        
        # Remove from loaded extensions
        if extension_id in self.extensions:
            del self.extensions[extension_id]
        
        return True
    
    def _save_extension_state(self, extension_id: str, enabled: bool) -> None:
        """Save extension state to a configuration file."""
        config_file = os.path.join(self.extension_dir, "extension_config.json")
        
        # Load existing config
        config = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
            except:
                pass
        
        # Update config
        if "enabled" not in config:
            config["enabled"] = []
        
        if enabled:
            if extension_id not in config["enabled"]:
                config["enabled"].append(extension_id)
        else:
            if extension_id in config["enabled"]:
                config["enabled"].remove(extension_id)
        
        # Save config
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    
    def _get_extension_state(self, extension_id: str) -> bool:
        """Get extension enabled state from configuration."""
        config_file = os.path.join(self.extension_dir, "extension_config.json")
        
        # Default state
        enabled = False
        
        # Load config if it exists
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    
                    # Check if the extension is enabled
                    if "enabled" in config and extension_id in config["enabled"]:
                        enabled = True
            except:
                pass
        
        return enabled

# Global registry instance
registry = ExtensionRegistry()

# Map the extension functions to the FastAPI routes
# These functions will be called by the route handlers in main.py

async def list_extensions():
    """List all installed extensions."""
    extensions = registry.get_all_extensions()
    
    result = []
    for extension_id, extension in extensions.items():
        result.append({
            "id": extension_id,
            "name": getattr(extension, "name", extension_id),
            "description": getattr(extension, "description", ""),
            "version": getattr(extension, "version", "0.0.0"),
            "author": getattr(extension, "author", ""),
            "enabled": extension.enabled,
            "installed": extension.installed,
        })
    
    return result

async def enable_extension(extension_id: str):
    """Enable an extension."""
    success = registry.enable_extension(extension_id)
    
    if not success:
        return {"status": "error", "message": f"Extension {extension_id} not found"}
    
    # Get the extension
    extension = registry.load_extension(extension_id)
    
    # Call the startup method
    try:
        await extension.startup()
    except Exception as e:
        return {"status": "error", "message": f"Error starting extension: {str(e)}"}
    
    return {"status": "success"}

async def disable_extension(extension_id: str):
    """Disable an extension."""
    # Get the extension
    extension = registry.load_extension(extension_id)
    
    if not extension:
        return {"status": "error", "message": f"Extension {extension_id} not found"}
    
    # Call the shutdown method
    try:
        await extension.shutdown()
    except Exception as e:
        print(f"Error shutting down extension: {str(e)}")
    
    # Disable the extension
    success = registry.disable_extension(extension_id)
    
    if not success:
        return {"status": "error", "message": f"Failed to disable extension {extension_id}"}
    
    return {"status": "success"}

async def install_extension(file_path: str):
    """Install an extension from a ZIP file."""
    # Install the extension
    extension_id = registry.install_extension(file_path)
    
    if not extension_id:
        return {"status": "error", "message": "Failed to install extension"}
    
    return {"status": "success", "extension_id": extension_id}

async def uninstall_extension(extension_id: str):
    """Uninstall an extension."""
    success = registry.uninstall_extension(extension_id)
    
    if not success:
        return {"status": "error", "message": f"Failed to uninstall extension {extension_id}"}
    
    return {"status": "success"}
'''
        
        ext_implementation_path = os.path.join(open_webui_path, "extensions.py")
        with open(ext_implementation_path, "w") as f:
            f.write(extensions_py_content)
        logger.info(f"Created extension implementation at {ext_implementation_path}")
        
        # Now, modify the main.py file to add our extension routes
        main_py_path = os.path.join(open_webui_path, "main.py")
        if not os.path.exists(main_py_path):
            logger.error(f"main.py not found at {main_py_path}")
            return False
        
        # Read the main.py file
        with open(main_py_path, "r") as f:
            main_content = f.read()
        
        # Prepare the code to inject
        routes_to_add = '''
# Extension System Routes
@app.get("/extensions/manager", response_class=HTMLResponse)
async def extension_manager():
    """Serve the extension manager UI."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "extensions", "manager.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Extension Manager not found</h1>")

@app.get("/extensions/api/list")
async def list_extensions():
    """List all installed extensions."""
    from extensions import list_extensions
    return await list_extensions()

@app.post("/extensions/api/{extension_id}/enable")
async def enable_extension(extension_id: str):
    """Enable an extension."""
    from extensions import enable_extension
    return await enable_extension(extension_id)

@app.post("/extensions/api/{extension_id}/disable")
async def disable_extension(extension_id: str):
    """Disable an extension."""
    from extensions import disable_extension
    return await disable_extension(extension_id)

@app.post("/extensions/api/install")
async def install_extension(file: UploadFile = File(...)):
    """Install an extension from a ZIP file."""
    # Save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
    
    try:
        # Install the extension
        from extensions import install_extension
        result = await install_extension(temp_path)
        
        # Clean up
        os.unlink(temp_path)
        
        return result
    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        return {"status": "error", "message": str(e)}

@app.delete("/extensions/api/{extension_id}/uninstall")
async def uninstall_extension(extension_id: str):
    """Uninstall an extension."""
    from extensions import uninstall_extension
    return await uninstall_extension(extension_id)
'''
        
        # Check if our routes are already in the file
        if "/extensions/manager" not in main_content:
            # Try to find a good place to insert our routes
            # The best place would be after the imports but before the first route definition
            
            # First, add the import for HTMLResponse if needed
            if "from fastapi.responses import HTMLResponse" not in main_content:
                new_import = "from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse"
                if "from fastapi.responses import JSONResponse, RedirectResponse" in main_content:
                    main_content = main_content.replace(
                        "from fastapi.responses import JSONResponse, RedirectResponse",
                        new_import
                    )
                else:
                    # Find a suitable place in the imports
                    import_section_end = main_content.find("from fastapi import")
                    # Find the end of import statements
                    next_newline = main_content.find("\n\n", import_section_end)
                    if next_newline != -1:
                        main_content = main_content[:next_newline] + "\nfrom fastapi.responses import HTMLResponse" + main_content[next_newline:]
            
            # Look for the app initialization
            app_init = main_content.find("app = FastAPI(")
            if app_init != -1:
                # Find the first route definition after app initialization
                route_start = main_content.find("@app.", app_init)
                if route_start != -1:
                    # Insert our routes before the first route
                    main_content = main_content[:route_start] + routes_to_add + "\n" + main_content[route_start:]
                else:
                    # If no routes found, add at the end of the file
                    main_content += "\n" + routes_to_add
            else:
                # If app initialization not found, add at the end of the file
                main_content += "\n" + routes_to_add
            
            # Write the modified file
            with open(main_py_path, "w") as f:
                f.write(main_content)
            
            logger.info(f"Added extension routes to {main_py_path}")
        else:
            logger.info("Extension routes already exist in main.py")
        
        logger.info("Extension manager integration successful!")
        logger.info("Access the extension manager at: /extensions/manager")
        
        return True
    
    except Exception as e:
        logger.error(f"Error setting up extension manager: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Open WebUI Extension Manager integration')
    parser.add_argument('--path', type=str, help='Path to Open WebUI installation')
    args = parser.parse_args()
    
    install_admin_integration(args.path)

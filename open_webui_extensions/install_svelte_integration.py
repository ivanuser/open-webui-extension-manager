import os
import logging
import argparse
import sys
import re
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("open_webui_extensions")

def install_svelte_integration(open_webui_path=None):
    """Install the Svelte UI integration into Open WebUI Settings."""
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
    
    # Search for the Settings.svelte file
    settings_files = []
    
    # Search patterns for the Settings.svelte file
    search_paths = [
        os.path.join(open_webui_path, "frontend", "src", "lib", "components", "admin", "Settings.svelte"),
        os.path.join(open_webui_path, "frontend", "src", "routes", "settings", "+page.svelte"),
        os.path.join(open_webui_path, "frontend", "src", "lib", "components", "Settings.svelte"),
    ]
    
    # Check specific paths first
    for path in search_paths:
        if os.path.exists(path):
            settings_files.append(path)
    
    # If not found, do a recursive search
    if not settings_files:
        for root, dirs, files in os.walk(open_webui_path):
            for file in files:
                if file.lower() == "settings.svelte":
                    settings_files.append(os.path.join(root, file))
    
    if not settings_files:
        logger.error("Could not find Settings.svelte file")
        return False
    
    logger.info(f"Found Settings.svelte files: {settings_files}")
    
    # Process each potential Settings.svelte file
    for settings_file in settings_files:
        logger.info(f"Processing {settings_file}")
        
        # Create a backup of the file
        backup_file = settings_file + ".bak"
        shutil.copy2(settings_file, backup_file)
        logger.info(f"Created backup at {backup_file}")
        
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for the sidebar items array
            # Common patterns might be: let menuItems = [...] or const menuItems = [...] or tabs = [...]
            menu_items_pattern = re.search(r'(?:let|const)\s+(\w+)\s*=\s*\[(.*?)\];', content, re.DOTALL)
            
            if menu_items_pattern:
                variable_name = menu_items_pattern.group(1)
                items_content = menu_items_pattern.group(2)
                
                logger.info(f"Found menu items array: {variable_name}")
                
                # Check if "Extensions" is already in the array
                if "Extensions" in items_content:
                    logger.info("Extensions menu item already exists")
                    continue
                
                # Determine the format of the array items
                if "icon:" in items_content:
                    # Format with icon and label properties
                    extension_item = '''
    {
        icon: "puzzle-piece",
        label: "Extensions",
        target: "extensions",
        handler: () => {
            // Create iframe for extensions manager
            const iframe = document.createElement('iframe');
            iframe.src = '/extensions/manager';
            iframe.style.width = '100%';
            iframe.style.height = '90vh';
            iframe.style.border = 'none';
            document.querySelector('.content-area')?.replaceChildren(iframe);
        }
    }'''
                elif "{ text:" in items_content or "{'text:" in items_content:
                    # Format with text and value properties
                    extension_item = '''
    { 
        text: "Extensions", 
        value: "extensions",
        handler: () => {
            // Create iframe for extensions manager
            const iframe = document.createElement('iframe');
            iframe.src = '/extensions/manager';
            iframe.style.width = '100%';
            iframe.style.height = '90vh';
            iframe.style.border = 'none';
            document.querySelector('.content-area')?.replaceChildren(iframe);
        }
    }'''
                else:
                    # Simple format with just strings
                    extension_item = '"Extensions"'
                
                # Add the extension item to the array
                items_end = content.find('];', menu_items_pattern.start())
                if items_end != -1:
                    # Check if the array ends with a comma
                    comma_needed = not items_content.rstrip().endswith(',')
                    new_item = (', ' if comma_needed else '') + extension_item
                    
                    new_content = content[:items_end] + new_item + content[items_end:]
                    
                    with open(settings_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    logger.info(f"Added Extensions menu item to {settings_file}")
                    return True
            
            # Look for the sidebar items in a different format
            # Sometimes they're defined as a series of <a> tags in the HTML
            sidebar_html_pattern = re.search(r'<div\s+class="(?:settings-sidebar|sidebar)">(.*?)</div>', content, re.DOTALL)
            
            if sidebar_html_pattern:
                sidebar_content = sidebar_html_pattern.group(1)
                logger.info("Found sidebar HTML section")
                
                # Check if "Extensions" is already in the sidebar
                if "Extensions" in sidebar_content:
                    logger.info("Extensions menu item already exists")
                    continue
                
                # Create the Extensions menu item HTML
                extensions_html = '''
    <a href="javascript:void(0)" 
       class="flex items-center p-2 text-gray-500 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 group"
       on:click={() => {
           // Create iframe for extensions manager
           const iframe = document.createElement('iframe');
           iframe.src = '/extensions/manager';
           iframe.style.width = '100%';
           iframe.style.height = '90vh';
           iframe.style.border = 'none';
           document.querySelector('.content-area')?.replaceChildren(iframe);
           active = 'extensions';
       }}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-gray-500 dark:text-gray-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.25 6.087c0-.355.186-.676.401-.959.221-.29.349-.634.349-1.003 0-1.036-1.007-1.875-2.25-1.875s-2.25.84-2.25 1.875c0 .369.128.713.349 1.003.215.283.401.604.401.959v0a.64.64 0 01-.657.643 48.39 48.39 0 01-4.163-.3c.186 1.613.293 3.25.315 4.907a.656.656 0 01-.658.663v0c-.355 0-.676-.186-.959-.401a1.647 1.647 0 00-1.003-.349c-1.036 0-1.875 1.007-1.875 2.25s.84 2.25 1.875 2.25c.369 0 .713-.128 1.003-.349.283-.215.604-.401.959-.401v0c.31 0 .555.26.532.57a48.039 48.039 0 01-.642 5.056c1.518.19 3.058.309 4.616.354a.64.64 0 00.657-.643v0c0-.355-.186-.676-.401-.959a1.647 1.647 0 01-.349-1.003c0-1.035 1.008-1.875 2.25-1.875 1.243 0 2.25.84 2.25 1.875 0 .369-.128.713-.349 1.003-.215.283-.4.604-.4.959v0c0 .333.277.599.61.58a48.1 48.1 0 005.427-.63 48.05 48.05 0 00.582-4.717.532.532 0 00-.533-.57v0c-.355 0-.676.186-.959.401-.29.221-.634.349-1.003.349-1.035 0-1.875-1.007-1.875-2.25s.84-2.25 1.875-2.25c.37 0 .713.128 1.003.349.283.215.604.401.96.401v0a.656.656 0 00.658-.663 48.422 48.422 0 00-.37-5.36c-1.886.342-3.81.574-5.766.689a.578.578 0 01-.61-.58v0z" />
        </svg>
        <span class="ml-3">Extensions</span>
    </a>'''
                
                # Find the last menu item
                last_item_end = sidebar_content.rfind('</a>')
                if last_item_end != -1:
                    last_item_end = content.find('</a>', sidebar_html_pattern.start()) + 4
                    
                    new_content = content[:last_item_end] + extensions_html + content[last_item_end:]
                    
                    with open(settings_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    logger.info(f"Added Extensions menu item to {settings_file}")
                    return True
            
            logger.warning(f"Could not find suitable location to add Extensions menu item in {settings_file}")
        
        except Exception as e:
            logger.error(f"Error processing {settings_file}: {str(e)}")
            # Restore the backup
            shutil.copy2(backup_file, settings_file)
            logger.info(f"Restored backup from {backup_file}")
    
    logger.error("Could not add Extensions menu item to any Settings.svelte file")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Install Open WebUI Extension Manager Svelte integration')
    parser.add_argument('--path', type=str, help='Path to Open WebUI installation')
    args = parser.parse_args()
    
    install_svelte_integration(args.path)

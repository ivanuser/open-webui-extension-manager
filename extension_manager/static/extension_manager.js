// Extension Manager UI Component

// Register the Extension Manager component when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Extension Manager loaded');
    
    // Check if we need to add the UI component
    if (window.location.pathname === '/admin/extensions') {
        // Create and initialize the Extension Manager UI
        initExtensionManager();
    }
    
    // Add the sidebar menu item if it doesn't exist yet
    const addMenuItem = () => {
        const adminMenu = document.querySelector('.admin-menu');
        if (adminMenu && !document.querySelector('.extension-manager-menu-item')) {
            const menuItem = document.createElement('div');
            menuItem.className = 'admin-menu-item extension-manager-menu-item';
            menuItem.innerHTML = `
                <span class="admin-menu-item-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="9" y1="3" x2="9" y2="21"></line>
                        <line x1="15" y1="3" x2="15" y2="21"></line>
                        <line x1="3" y1="9" x2="21" y2="9"></line>
                        <line x1="3" y1="15" x2="21" y2="15"></line>
                    </svg>
                </span>
                <span class="admin-menu-item-text">Extensions</span>
            `;
            menuItem.addEventListener('click', () => {
                window.location.href = '/admin/extensions';
            });
            adminMenu.appendChild(menuItem);
        }
    };
    
    // Try to add the menu item now and retry after a delay
    addMenuItem();
    setTimeout(addMenuItem, 1000);
    setTimeout(addMenuItem, 3000);
});

// Initialize the Extension Manager UI
function initExtensionManager() {
    console.log('Initializing Extension Manager UI');
    
    // Find or create the main container
    const mainContainer = document.querySelector('main') || document.body;
    if (!mainContainer) return;
    
    // Clear the main container
    mainContainer.innerHTML = '';
    
    // Create the Extension Manager container
    const container = document.createElement('div');
    container.className = 'extension-manager-container';
    mainContainer.appendChild(container);
    
    // Add styles
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .extension-manager-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .extension-manager-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .extension-manager-header h2 {
            margin: 0;
            color: var(--text-color, #333);
        }
        
        .extension-card {
            background: var(--card-background, #fff);
            border: 1px solid var(--border-color, #ddd);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.2s;
        }
        
        .extension-card:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .extension-card.disabled {
            opacity: 0.7;
        }
        
        .btn {
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: var(--primary-color, #007bff);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--primary-color-dark, #0069d9);
        }
    `;
    document.head.appendChild(styleElement);
    
    // Add the Extension Manager UI
    container.innerHTML = `
        <div class="extension-manager-header">
            <h2>Extension Manager</h2>
            <button id="install-extension-btn" class="btn btn-primary">Install Extension</button>
        </div>
        
        <div id="extensions-container">
            <p>Loading extensions...</p>
        </div>
    `;
    
    // Add event listeners
    document.getElementById('install-extension-btn').addEventListener('click', () => {
        alert('Install Extension functionality will be implemented here.');
    });
    
    // Load extensions
    loadExtensions();
}

// Load extensions from the API
async function loadExtensions() {
    const extensionsContainer = document.getElementById('extensions-container');
    
    try {
        const response = await fetch('/api/extensions/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const extensions = data.extensions || [];
        
        if (extensions.length === 0) {
            extensionsContainer.innerHTML = '<p>No extensions installed.</p>';
            return;
        }
        
        extensionsContainer.innerHTML = '';
        
        extensions.forEach(extension => {
            const extensionCard = document.createElement('div');
            extensionCard.className = `extension-card ${extension.enabled ? '' : 'disabled'}`;
            
            extensionCard.innerHTML = `
                <h3>${extension.name} <small>v${extension.version}</small></h3>
                <p>${extension.description}</p>
                <p><strong>Author:</strong> ${extension.author}</p>
                <div class="extension-actions">
                    <label class="switch">
                        <input type="checkbox" ${extension.enabled ? 'checked' : ''} data-id="${extension.id}" class="extension-toggle">
                        <span class="slider"></span>
                        ${extension.enabled ? 'Enabled' : 'Disabled'}
                    </label>
                    <button class="btn btn-danger" data-id="${extension.id}">Delete</button>
                </div>
            `;
            
            extensionsContainer.appendChild(extensionCard);
        });
        
        // Add event listeners for toggle switches
        document.querySelectorAll('.extension-toggle').forEach(toggle => {
            toggle.addEventListener('change', async (e) => {
                const extensionId = e.target.dataset.id;
                const enabled = e.target.checked;
                
                // Call the API to toggle the extension
                try {
                    const response = await fetch(`/api/extensions/${extensionId}/toggle`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ enable: enabled })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    // Reload extensions
                    loadExtensions();
                } catch (error) {
                    console.error('Error toggling extension:', error);
                    alert(`Error toggling extension: ${error.message}`);
                }
            });
        });
    } catch (error) {
        console.error('Error loading extensions:', error);
        extensionsContainer.innerHTML = `<p>Error loading extensions: ${error.message}</p>`;
    }
}

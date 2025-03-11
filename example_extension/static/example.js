// Example Extension JavaScript

console.log("Example Extension loaded");

// Add the example component to the page when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if we need to add the UI component
    if (window.location.pathname === '/admin/example') {
        // Create and initialize the Example UI
        initExampleUI();
    }
    
    // Add the admin menu item if it doesn't exist yet
    const addMenuItem = () => {
        const adminMenu = document.querySelector('.admin-menu');
        if (adminMenu && !document.querySelector('.example-extension-menu-item')) {
            const menuItem = document.createElement('div');
            menuItem.className = 'admin-menu-item example-extension-menu-item';
            menuItem.innerHTML = `
                <span class="admin-menu-item-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </span>
                <span class="admin-menu-item-text">Example Extension</span>
            `;
            menuItem.addEventListener('click', () => {
                window.location.href = '/admin/example';
            });
            adminMenu.appendChild(menuItem);
        }
    };
    
    // Try to add the menu item now and retry after a delay
    addMenuItem();
    setTimeout(addMenuItem, 1000);
    setTimeout(addMenuItem, 3000);
});

// Initialize the Example UI
function initExampleUI() {
    console.log('Initializing Example UI');
    
    // Find or create the main container
    const mainContainer = document.querySelector('main') || document.body;
    if (!mainContainer) return;
    
    // Clear the main container
    mainContainer.innerHTML = '';
    
    // Create the Example container
    const container = document.createElement('div');
    container.className = 'example-extension-container';
    container.style.maxWidth = '800px';
    container.style.margin = '0 auto';
    container.style.padding = '20px';
    
    container.innerHTML = `
        <div style="background: var(--background-color, #fff); border-radius: 8px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2>Example Extension</h2>
            <p>This is an example extension for Open WebUI. It demonstrates how to create extensions for Open WebUI.</p>
            
            <div style="background: var(--background-secondary, #f5f5f5); border-radius: 8px; padding: 20px; margin-top: 20px;">
                <h3>Extension Features</h3>
                <ul>
                    <li>Adding custom UI components</li>
                    <li>Providing API endpoints</li>
                    <li>Registering admin pages</li>
                    <li>Loading static assets</li>
                </ul>
            </div>
            
            <div style="background: var(--background-secondary, #f5f5f5); border-radius: 8px; padding: 20px; margin-top: 20px;">
                <h3>API Example</h3>
                <p>This extension provides a simple API endpoint:</p>
                <pre style="background: var(--background-tertiary, #eee); padding: 10px; border-radius: 4px;">/api/ext/example/hello</pre>
                <button id="test-api-btn" style="background: var(--primary-color, #007bff); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-top: 10px;">
                    Test API Endpoint
                </button>
                <div id="api-result" style="margin-top: 10px;"></div>
            </div>
        </div>
    `;
    
    mainContainer.appendChild(container);
    
    // Add event listeners
    document.getElementById('test-api-btn').addEventListener('click', async () => {
        const resultElement = document.getElementById('api-result');
        resultElement.innerHTML = 'Loading...';
        
        try {
            const response = await fetch('/api/ext/example/hello');
            const data = await response.json();
            
            resultElement.innerHTML = `
                <div style="background: var(--success-color-light, #d4edda); color: var(--success-color, #28a745); padding: 10px; border-radius: 4px;">
                    API Response: ${JSON.stringify(data)}
                </div>
            `;
        } catch (error) {
            resultElement.innerHTML = `
                <div style="background: var(--danger-color-light, #f8d7da); color: var(--danger-color, #dc3545); padding: 10px; border-radius: 4px;">
                    Error: ${error.message}
                </div>
            `;
        }
    });
}

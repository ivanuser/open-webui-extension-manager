// MCP Manager UI Component

// Register the MCP Manager component
document.addEventListener('DOMContentLoaded', () => {
    console.log('MCP Manager loaded');
    
    // Check if we're on the MCP page
    if (window.location.pathname === '/mcp') {
        initMCPManager();
    }
    
    // Add the sidebar menu item if it doesn't exist yet
    const addMenuItem = () => {
        const sidebar = document.querySelector('.sidebar-menu');
        if (sidebar && !document.querySelector('.mcp-menu-item')) {
            const menuItem = document.createElement('div');
            menuItem.className = 'sidebar-menu-item mcp-menu-item';
            menuItem.innerHTML = `
                <span class="sidebar-menu-item-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
                        <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
                        <line x1="6" y1="6" x2="6.01" y2="6"></line>
                        <line x1="6" y1="18" x2="6.01" y2="18"></line>
                    </svg>
                </span>
                <span class="sidebar-menu-item-text">MCP Servers</span>
            `;
            
            menuItem.addEventListener('click', () => {
                window.location.href = '/mcp';
            });
            
            sidebar.appendChild(menuItem);
        }
    };
    
    // Try to add the menu item now and retry after a delay
    addMenuItem();
    setTimeout(addMenuItem, 1000);
    setTimeout(addMenuItem, 3000);
});

// Initialize the MCP Manager
function initMCPManager() {
    console.log('Initializing MCP Manager');
    
    // Find or create the main container
    const mainContainer = document.querySelector('main') || document.body;
    if (!mainContainer) return;
    
    // Clear the main container
    mainContainer.innerHTML = '';
    
    // Create the MCP Manager container
    const container = document.createElement('div');
    container.className = 'mcp-manager-container';
    container.style.maxWidth = '1200px';
    container.style.margin = '0 auto';
    container.style.padding = '20px';
    
    // Add styles
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .mcp-server-card {
            background: var(--card-background, #fff);
            border: 1px solid var(--border-color, #ddd);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.2s;
        }
        
        .mcp-server-card:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .mcp-server-card.disabled {
            opacity: 0.7;
        }
        
        .mcp-server-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .mcp-server-title {
            font-size: 18px;
            margin: 0;
        }
        
        .mcp-server-status {
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 4px;
            margin-left: 10px;
        }
        
        .mcp-status-connected {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
        }
        
        .mcp-status-disconnected {
            background: rgba(220, 53, 69, 0.1);
            color: #dc3545;
        }
        
        .mcp-status-disabled {
            background: rgba(108, 117, 125, 0.1);
            color: #6c757d;
        }
        
        .mcp-server-url {
            font-family: monospace;
            font-size: 14px;
            color: var(--text-secondary, #666);
            margin-bottom: 10px;
        }
        
        .mcp-server-actions {
            display: flex;
            gap: 8px;
        }
        
        .mcp-btn {
            padding: 6px 12px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .mcp-btn-primary {
            background: var(--primary-color, #007bff);
            color: white;
        }
        
        .mcp-btn-secondary {
            background: var(--background-secondary, #f5f5f5);
            color: var(--text-primary, #333);
            border: 1px solid var(--border-color, #ddd);
        }
        
        .mcp-btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .mcp-switch {
            position: relative;
            display: inline-block;
            width: 40px;
            height: 20px;
            margin-right: 8px;
        }
        
        .mcp-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .mcp-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 20px;
        }
        
        .mcp-slider:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .mcp-slider {
            background-color: var(--primary-color, #007bff);
        }
        
        input:focus + .mcp-slider {
            box-shadow: 0 0 1px var(--primary-color, #007bff);
        }
        
        input:checked + .mcp-slider:before {
            transform: translateX(20px);
        }
        
        .mcp-model-card {
            background: var(--background-secondary, #f5f5f5);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .mcp-model-name {
            font-weight: 500;
            margin: 0;
        }
        
        .mcp-model-server {
            font-size: 12px;
            color: var(--text-secondary, #666);
        }
        
        .mcp-empty-state {
            text-align: center;
            padding: 40px 20px;
            background: var(--background-secondary, #f5f5f5);
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .mcp-server-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .mcp-modal-content {
            background: var(--background-primary, #fff);
            border-radius: 8px;
            padding: 20px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .mcp-form-group {
            margin-bottom: 15px;
        }
        
        .mcp-form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        .mcp-form-group input, .mcp-form-group textarea {
            width: 100%;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid var(--border-color, #ddd);
            background: var(--background-primary, #fff);
        }
        
        .mcp-form-group textarea {
            min-height: 80px;
            resize: vertical;
        }
    `;
    document.head.appendChild(styleElement);
    
    // Add the MCP Manager content
    container.innerHTML = `
        <h2>MCP Servers</h2>
        <p>Connect to MCP (Model Context Protocol) servers to access additional models.</p>
        
        <div id="mcp-alert-container" style="margin-top: 15px;"></div>
        
        <div style="display: flex; justify-content: flex-end; margin: 20px 0;">
            <button id="mcp-add-server-btn" class="mcp-btn mcp-btn-primary">Add Server</button>
        </div>
        
        <div id="mcp-servers-container">
            <div style="text-align: center; padding: 20px;">
                <div style="border: 4px solid rgba(0, 0, 0, 0.1); border-radius: 50%; border-top-color: var(--primary-color, #007bff); width: 30px; height: 30px; animation: mcp-spin 1s linear infinite; margin: 0 auto;"></div>
                <p style="margin-top: 10px;">Loading servers...</p>
            </div>
        </div>
        
        <h3 style="margin-top: 30px;">Available Models</h3>
        <div id="mcp-models-container">
            <div style="text-align: center; padding: 20px;">
                <div style="border: 4px solid rgba(0, 0, 0, 0.1); border-radius: 50%; border-top-color: var(--primary-color, #007bff); width: 30px; height: 30px; animation: mcp-spin 1s linear infinite; margin: 0 auto;"></div>
                <p style="margin-top: 10px;">Loading models...</p>
            </div>
        </div>
        
        <div id="mcp-server-modal" class="mcp-server-modal">
            <div class="mcp-modal-content">
                <h3 id="mcp-modal-title">Add MCP Server</h3>
                
                <form id="mcp-server-form">
                    <div class="mcp-form-group">
                        <label for="mcp-server-name">Server Name</label>
                        <input type="text" id="mcp-server-name" required>
                    </div>
                    
                    <div class="mcp-form-group">
                        <label for="mcp-server-url">Server URL</label>
                        <input type="url" id="mcp-server-url" required placeholder="https://example.com/v1">
                        <div style="font-size: 12px; color: var(--text-secondary, #666); margin-top: 3px;">Include the base path (e.g., /v1)</div>
                    </div>
                    
                    <div class="mcp-form-group">
                        <label for="mcp-server-api-key">API Key (optional)</label>
                        <input type="password" id="mcp-server-api-key">
                    </div>
                    
                    <div class="mcp-form-group">
                        <label for="mcp-server-description">Description (optional)</label>
                        <textarea id="mcp-server-description"></textarea>
                    </div>
                    
                    <div class="mcp-form-group">
                        <label style="display: flex; align-items: center;">
                            <input type="checkbox" id="mcp-server-enabled" checked style="width: auto; margin-right: 8px;">
                            Enabled
                        </label>
                    </div>
                    
                    <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
                        <button type="button" id="mcp-cancel-btn" class="mcp-btn mcp-btn-secondary">Cancel</button>
                        <button type="submit" class="mcp-btn mcp-btn-primary">Save</button>
                    </div>
                </form>
            </div>
        </div>
        
        <style>
            @keyframes mcp-spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    
    mainContainer.appendChild(container);
    
    // Add event listeners
    document.getElementById('mcp-add-server-btn').addEventListener('click', () => {
        showServerModal();
    });
    
    document.getElementById('mcp-cancel-btn').addEventListener('click', () => {
        closeServerModal();
    });
    
    document.getElementById('mcp-server-form').addEventListener('submit', (e) => {
        e.preventDefault();
        saveServer();
    });
    
    // Load servers and models
    loadServers();
    loadModels();
}

// Global variables
let editingServer = null;

// Show the server modal
function showServerModal(server = null) {
    const modal = document.getElementById('mcp-server-modal');
    const modalTitle = document.getElementById('mcp-modal-title');
    const nameInput = document.getElementById('mcp-server-name');
    const urlInput = document.getElementById('mcp-server-url');
    const apiKeyInput = document.getElementById('mcp-server-api-key');
    const descriptionInput = document.getElementById('mcp-server-description');
    const enabledInput = document.getElementById('mcp-server-enabled');
    
    // Reset form
    document.getElementById('mcp-server-form').reset();
    
    if (server) {
        // Editing existing server
        modalTitle.textContent = 'Edit MCP Server';
        nameInput.value = server.name;
        urlInput.value = server.url;
        descriptionInput.value = server.description || '';
        enabledInput.checked = server.enabled;
        
        // Save the server name for editing
        editingServer = server.name;
    } else {
        // Adding new server
        modalTitle.textContent = 'Add MCP Server';
        editingServer = null;
    }
    
    modal.style.display = 'flex';
}

// Close the server modal
function closeServerModal() {
    document.getElementById('mcp-server-modal').style.display = 'none';
    editingServer = null;
}

// Save the server
async function saveServer() {
    const nameInput = document.getElementById('mcp-server-name');
    const urlInput = document.getElementById('mcp-server-url');
    const apiKeyInput = document.getElementById('mcp-server-api-key');
    const descriptionInput = document.getElementById('mcp-server-description');
    const enabledInput = document.getElementById('mcp-server-enabled');
    
    const serverData = {
        name: nameInput.value,
        url: urlInput.value,
        api_key: apiKeyInput.value,
        description: descriptionInput.value,
        enabled: enabledInput.checked
    };
    
    try {
        let response;
        
        if (editingServer) {
            // Update existing server
            response = await fetch(`/api/ext/mcp_connector/servers/${encodeURIComponent(editingServer)}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(serverData)
            });
        } else {
            // Create new server
            response = await fetch('/api/ext/mcp_connector/servers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(serverData)
            });
        }
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        // Close the modal and reload servers
        closeServerModal();
        showAlert(`Server ${editingServer ? 'updated' : 'added'} successfully!`, 'success');
        await loadServers();
        await loadModels();
    } catch (error) {
        console.error('Error saving server:', error);
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Load servers from the API
async function loadServers() {
    const serversContainer = document.getElementById('mcp-servers-container');
    
    try {
        const response = await fetch('/api/ext/mcp_connector/servers');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const servers = await response.json();
        
        if (servers.length === 0) {
            serversContainer.innerHTML = `
                <div class="mcp-empty-state">
                    <p>No MCP servers configured. Click "Add Server" to get started.</p>
                </div>
            `;
            return;
        }
        
        serversContainer.innerHTML = '';
        
        servers.forEach(server => {
            const serverCard = document.createElement('div');
            serverCard.className = `mcp-server-card ${server.enabled ? '' : 'disabled'}`;
            
            let statusClass = '';
            if (server.status === 'Connected') {
                statusClass = 'mcp-status-connected';
            } else if (server.status === 'Disabled') {
                statusClass = 'mcp-status-disabled';
            } else {
                statusClass = 'mcp-status-disconnected';
            }
            
            serverCard.innerHTML = `
                <div class="mcp-server-header">
                    <h3 class="mcp-server-title">
                        ${server.name}
                        <span class="mcp-server-status ${statusClass}">${server.status}</span>
                    </h3>
                    <div class="mcp-server-actions">
                        <label class="mcp-switch">
                            <input type="checkbox" class="mcp-server-toggle" data-name="${server.name}" ${server.enabled ? 'checked' : ''}>
                            <span class="mcp-slider"></span>
                        </label>
                        <button class="mcp-btn mcp-btn-secondary mcp-test-btn" data-name="${server.name}">Test</button>
                        <button class="mcp-btn mcp-btn-secondary mcp-edit-btn" data-name="${server.name}">Edit</button>
                        <button class="mcp-btn mcp-btn-danger mcp-delete-btn" data-name="${server.name}">Delete</button>
                    </div>
                </div>
                <div class="mcp-server-url">${server.url}</div>
                ${server.description ? `<p>${server.description}</p>` : ''}
            `;
            
            serversContainer.appendChild(serverCard);
        });
        
        // Add event listeners
        document.querySelectorAll('.mcp-server-toggle').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                toggleServer(e.target.dataset.name, e.target.checked);
            });
        });
        
        document.querySelectorAll('.mcp-test-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                testServer(e.target.dataset.name);
            });
        });
        
        document.querySelectorAll('.mcp-edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                editServer(e.target.dataset.name);
            });
        });
        
        document.querySelectorAll('.mcp-delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                deleteServer(e.target.dataset.name);
            });
        });
    } catch (error) {
        console.error('Error loading servers:', error);
        serversContainer.innerHTML = `
            <div style="background: rgba(220, 53, 69, 0.1); color: #dc3545; padding: 15px; border-radius: 8px; margin-top: 15px;">
                Error loading servers: ${error.message}
            </div>
        `;
    }
}

// Load models from the API
async function loadModels() {
    const modelsContainer = document.getElementById('mcp-models-container');
    
    try {
        const response = await fetch('/api/ext/mcp_connector/models');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const models = await response.json();
        
        if (models.length === 0) {
            modelsContainer.innerHTML = `
                <div class="mcp-empty-state">
                    <p>No models available. Enable an MCP server to see available models.</p>
                </div>
            `;
            return;
        }
        
        modelsContainer.innerHTML = '';
        
        models.forEach(model => {
            const modelCard = document.createElement('div');
            modelCard.className = 'mcp-model-card';
            
            modelCard.innerHTML = `
                <div>
                    <h4 class="mcp-model-name">${model.name}</h4>
                    <div class="mcp-model-server">Server: ${model.server}</div>
                </div>
            `;
            
            modelsContainer.appendChild(modelCard);
        });
    } catch (error) {
        console.error('Error loading models:', error);
        modelsContainer.innerHTML = `
            <div style="background: rgba(220, 53, 69, 0.1); color: #dc3545; padding: 15px; border-radius: 8px; margin-top: 15px;">
                Error loading models: ${error.message}
            </div>
        `;
    }
}

// Test a server connection
async function testServer(serverName) {
    try {
        const response = await fetch(`/api/ext/mcp_connector/servers/${encodeURIComponent(serverName)}/test`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        showAlert(`${result.status}: ${result.message}`, result.status === 'Connected' ? 'success' : 'danger');
        
        // Reload servers to update status
        await loadServers();
    } catch (error) {
        console.error('Error testing server:', error);
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Toggle server enabled/disabled
async function toggleServer(serverName, enabled) {
    try {
        const response = await fetch(`/api/ext/mcp_connector/servers/${encodeURIComponent(serverName)}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enable: enabled })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Reload servers and models
        await loadServers();
        await loadModels();
        
        showAlert(`Server ${enabled ? 'enabled' : 'disabled'} successfully!`, 'success');
    } catch (error) {
        console.error('Error toggling server:', error);
        showAlert(`Error: ${error.message}`, 'danger');
        
        // Reload servers to reset toggle state
        await loadServers();
    }
}

// Edit a server
async function editServer(serverName) {
    try {
        const response = await fetch('/api/ext/mcp_connector/servers');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const servers = await response.json();
        const server = servers.find(s => s.name === serverName);
        
        if (server) {
            showServerModal(server);
        } else {
            throw new Error(`Server '${serverName}' not found`);
        }
    } catch (error) {
        console.error('Error editing server:', error);
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Delete a server
async function deleteServer(serverName) {
    if (!confirm(`Are you sure you want to delete the server "${serverName}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/ext/mcp_connector/servers/${encodeURIComponent(serverName)}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Reload servers and models
        await loadServers();
        await loadModels();
        
        showAlert(`Server deleted successfully!`, 'success');
    } catch (error) {
        console.error('Error deleting server:', error);
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Show an alert message
function showAlert(message, type) {
    const alertContainer = document.getElementById('mcp-alert-container');
    
    const alert = document.createElement('div');
    alert.style.padding = '10px 15px';
    alert.style.borderRadius = '8px';
    alert.style.marginBottom = '15px';
    alert.style.position = 'relative';
    
    if (type === 'success') {
        alert.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
        alert.style.color = '#28a745';
        alert.style.border = '1px solid rgba(40, 167, 69, 0.2)';
    } else {
        alert.style.backgroundColor = 'rgba(220, 53, 69, 0.1)';
        alert.style.color = '#dc3545';
        alert.style.border = '1px solid rgba(220, 53, 69, 0.2)';
    }
    
    alert.innerHTML = `
        ${message}
        <button style="position: absolute; top: 5px; right: 10px; background: transparent; border: none; color: inherit; font-size: 16px; cursor: pointer;">×</button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Add event listener to close button
    alert.querySelector('button').addEventListener('click', () => {
        alert.remove();
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

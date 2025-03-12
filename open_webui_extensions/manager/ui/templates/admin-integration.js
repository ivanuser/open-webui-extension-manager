/**
 * Admin Integration Script for Open WebUI Extension Manager
 * 
 * This script injects the Extension Manager into the Open WebUI admin interface
 */
(function() {
    // Wait for the admin interface to be fully loaded
    function waitForAdminInterface() {
        // Look for the admin sidebar
        const sidebar = document.querySelector('.admin-sidebar');
        if (!sidebar) {
            setTimeout(waitForAdminInterface, 500);
            return;
        }
        
        // Add the Extensions menu item
        addExtensionsMenuItem(sidebar);
    }
    
    // Add the Extensions menu item to the sidebar
    function addExtensionsMenuItem(sidebar) {
        // Create the menu item
        const menuItem = document.createElement('a');
        menuItem.href = '#extensions';
        menuItem.className = 'admin-sidebar-item';
        menuItem.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5">
                <path d="M18 20V6a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14"></path>
                <path d="M2 20h20"></path>
                <path d="M14 12v.01"></path>
            </svg>
            <span>Extensions</span>
        `;
        
        // Add to sidebar
        sidebar.appendChild(menuItem);
        
        // Handle click event
        menuItem.addEventListener('click', function(e) {
            e.preventDefault();
            showExtensionsPanel();
        });
        
        // If the URL hash is #extensions, show the panel
        if (window.location.hash === '#extensions') {
            showExtensionsPanel();
        }
    }
    
    // Show the Extensions panel
    function showExtensionsPanel() {
        // Hide all content panels
        document.querySelectorAll('.admin-content').forEach(el => {
            el.style.display = 'none';
        });
        
        // Deactivate all sidebar items
        document.querySelectorAll('.admin-sidebar-item').forEach(el => {
            el.classList.remove('active');
        });
        
        // Activate the Extensions sidebar item
        document.querySelector('a[href="#extensions"]').classList.add('active');
        
        // Create or show the Extensions panel
        let extensionsPanel = document.getElementById('admin-extensions-panel');
        
        if (!extensionsPanel) {
            // Create the panel
            extensionsPanel = document.createElement('div');
            extensionsPanel.id = 'admin-extensions-panel';
            extensionsPanel.className = 'admin-content';
            
            // Add the iframe
            const iframe = document.createElement('iframe');
            iframe.src = '/api/_extensions/ui/';
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.border = 'none';
            
            extensionsPanel.appendChild(iframe);
            
            // Add to the admin container
            document.querySelector('.admin-container').appendChild(extensionsPanel);
        }
        
        // Show the panel
        extensionsPanel.style.display = 'block';
        
        // Update the URL hash
        window.location.hash = 'extensions';
    }
    
    // Start the integration
    waitForAdminInterface();
})();

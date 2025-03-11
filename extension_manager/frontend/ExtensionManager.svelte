<!-- Extension Manager Main Component -->
<script>
  import { onMount } from 'svelte';
  import ExtensionCard from './ExtensionCard.svelte';
  import ExtensionForm from './ExtensionForm.svelte';

  // State
  let extensions = [];
  let loading = true;
  let error = null;
  let showInstallForm = false;
  let filters = {
    types: [],
    status: [],
    sources: [],
    search: ''
  };
  let pagination = {
    page: 1,
    pageSize: 10,
    total: 0
  };

  // Fetch extensions from API
  async function fetchExtensions() {
    loading = true;
    error = null;
    
    try {
      // Build query params
      const queryParams = new URLSearchParams();
      
      // Add filters
      if (filters.types.length > 0) {
        filters.types.forEach(type => queryParams.append('types', type));
      }
      if (filters.status.length > 0) {
        filters.status.forEach(status => queryParams.append('status', status));
      }
      if (filters.sources.length > 0) {
        filters.sources.forEach(source => queryParams.append('sources', source));
      }
      if (filters.search) {
        queryParams.append('search', filters.search);
      }
      
      // Add pagination
      queryParams.append('page', pagination.page);
      queryParams.append('page_size', pagination.pageSize);
      
      // Make API request
      const response = await fetch(`/api/extensions?${queryParams.toString()}`);
      const data = await response.json();
      
      if (data.success) {
        extensions = data.extensions;
        pagination.total = data.total;
      } else {
        error = data.message || 'Failed to fetch extensions';
      }
    } catch (err) {
      error = err.message || 'Failed to fetch extensions';
    } finally {
      loading = false;
    }
  }

  // Handle extension actions (enable, disable, uninstall)
  async function handleExtensionAction(event) {
    const { name, action } = event.detail;
    
    try {
      const response = await fetch('/api/extensions/action', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, action })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Update the extension in the list
        if (action === 'uninstall') {
          extensions = extensions.filter(ext => ext.name !== name);
          pagination.total -= 1;
        } else {
          const index = extensions.findIndex(ext => ext.name === name);
          if (index !== -1 && data.extension) {
            extensions[index] = data.extension;
            extensions = [...extensions]; // Trigger reactivity
          }
        }
      } else {
        error = data.message || `Failed to ${action} extension`;
      }
    } catch (err) {
      error = err.message || `Failed to ${action} extension`;
    }
  }

  // Install a new extension
  async function handleInstallExtension(event) {
    const installInfo = event.detail;
    
    try {
      const response = await fetch('/api/extensions/install', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(installInfo)
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Add the new extension to the list
        if (data.extension) {
          extensions = [...extensions, data.extension];
          pagination.total += 1;
        }
        showInstallForm = false;
      } else {
        error = data.message || 'Failed to install extension';
      }
    } catch (err) {
      error = err.message || 'Failed to install extension';
    }
  }

  // Update extension settings
  async function handleUpdateSettings(event) {
    const { name, settings } = event.detail;
    
    try {
      const response = await fetch('/api/extensions/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, settings })
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Update the extension in the list
        const index = extensions.findIndex(ext => ext.name === name);
        if (index !== -1 && data.extension) {
          extensions[index] = data.extension;
          extensions = [...extensions]; // Trigger reactivity
        }
      } else {
        error = data.message || 'Failed to update settings';
      }
    } catch (err) {
      error = err.message || 'Failed to update settings';
    }
  }

  // Update filters
  function handleFilterChange(event) {
    const { name, value } = event.target;
    filters[name] = value;
    pagination.page = 1; // Reset to first page when filters change
    fetchExtensions();
  }

  // Handle pagination
  function handlePageChange(page) {
    pagination.page = page;
    fetchExtensions();
  }

  // Load extensions on mount
  onMount(() => {
    fetchExtensions();
  });
</script>

<div class="extension-manager">
  <header class="extension-manager__header">
    <h1>Extension Manager</h1>
    <div class="extension-manager__actions">
      <button class="btn btn-primary" on:click={() => showInstallForm = true}>
        Install Extension
      </button>
      <button class="btn btn-secondary" on:click={fetchExtensions}>
        Refresh
      </button>
    </div>
  </header>

  {#if error}
    <div class="alert alert-danger">
      {error}
      <button class="alert-close" on:click={() => error = null}>×</button>
    </div>
  {/if}

  <div class="extension-manager__filters">
    <div class="filter-group">
      <label for="search">Search</label>
      <input 
        type="text" 
        id="search" 
        name="search" 
        bind:value={filters.search} 
        on:input={handleFilterChange}
        placeholder="Search extensions..."
      />
    </div>
    
    <div class="filter-group">
      <label>Type</label>
      <div class="checkbox-group">
        {#each ['ui', 'api', 'model', 'tool', 'theme', 'generic'] as type}
          <label>
            <input 
              type="checkbox" 
              bind:group={filters.types} 
              value={type} 
              on:change={handleFilterChange}
            />
            {type}
          </label>
        {/each}
      </div>
    </div>
    
    <div class="filter-group">
      <label>Status</label>
      <div class="checkbox-group">
        {#each ['active', 'inactive', 'error', 'pending'] as status}
          <label>
            <input 
              type="checkbox" 
              bind:group={filters.status} 
              value={status} 
              on:change={handleFilterChange}
            />
            {status}
          </label>
        {/each}
      </div>
    </div>
  </div>

  {#if loading}
    <div class="loading">Loading extensions...</div>
  {:else if extensions.length === 0}
    <div class="empty-state">
      <p>No extensions found. Install your first extension to get started.</p>
    </div>
  {:else}
    <div class="extension-list">
      {#each extensions as extension (extension.name)}
        <ExtensionCard 
          {extension} 
          on:action={handleExtensionAction}
          on:updateSettings={handleUpdateSettings}
        />
      {/each}
    </div>
    
    <div class="pagination">
      <button 
        class="btn btn-sm" 
        disabled={pagination.page === 1}
        on:click={() => handlePageChange(pagination.page - 1)}
      >
        Previous
      </button>
      
      <span class="pagination-info">
        Page {pagination.page} of {Math.ceil(pagination.total / pagination.pageSize)}
        ({pagination.total} extensions)
      </span>
      
      <button 
        class="btn btn-sm"
        disabled={pagination.page >= Math.ceil(pagination.total / pagination.pageSize)}
        on:click={() => handlePageChange(pagination.page + 1)}
      >
        Next
      </button>
    </div>
  {/if}

  {#if showInstallForm}
    <div class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Install Extension</h2>
          <button class="modal-close" on:click={() => showInstallForm = false}>×</button>
        </div>
        <div class="modal-body">
          <ExtensionForm 
            on:submit={handleInstallExtension}
            on:cancel={() => showInstallForm = false}
          />
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .extension-manager {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .extension-manager__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .extension-manager__actions {
    display: flex;
    gap: 0.5rem;
  }

  .extension-manager__filters {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 0.5rem;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .extension-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }

  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
  }

  .loading, .empty-state {
    text-align: center;
    padding: 2rem;
    color: #666;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .modal-content {
    background-color: white;
    border-radius: 0.5rem;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #eee;
  }

  .modal-body {
    padding: 1rem;
  }

  .alert {
    padding: 1rem;
    border-radius: 0.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .btn {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    cursor: pointer;
    font-weight: 500;
    border: none;
  }

  .btn-primary {
    background-color: #007bff;
    color: white;
  }

  .btn-secondary {
    background-color: #6c757d;
    color: white;
  }

  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
  }

  .btn:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }
</style>

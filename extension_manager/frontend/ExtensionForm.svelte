<!-- Extension Installation Form Component -->
<script>
  import { createEventDispatcher } from 'svelte';

  // Event dispatcher
  const dispatch = createEventDispatcher();

  // Form state
  let source = 'remote';
  let url = '';
  let path = '';
  let name = '';
  let loading = false;
  let error = null;

  // Handle form submission
  async function handleSubmit() {
    error = null;
    
    // Validate required fields based on source
    if (source === 'remote' && !url) {
      error = 'URL is required for remote installations';
      return;
    }
    
    if (source === 'local' && !path) {
      error = 'Path is required for local installations';
      return;
    }
    
    if (source === 'marketplace' && !name) {
      error = 'Extension name is required for marketplace installations';
      return;
    }
    
    // Create installation info
    const installInfo = {
      source,
      url: source === 'remote' ? url : undefined,
      path: source === 'local' ? path : undefined,
      name: source === 'marketplace' ? name : undefined,
    };
    
    // Dispatch submit event
    dispatch('submit', installInfo);
  }

  // Handle form cancel
  function handleCancel() {
    dispatch('cancel');
  }
</script>

<form class="extension-form" on:submit|preventDefault={handleSubmit}>
  {#if error}
    <div class="alert alert-danger">
      {error}
      <button type="button" class="alert-close" on:click={() => error = null}>×</button>
    </div>
  {/if}

  <div class="form-group">
    <label for="source">Installation Source</label>
    <select id="source" bind:value={source}>
      <option value="remote">Remote URL (ZIP file)</option>
      <option value="local">Local Directory</option>
      <option value="marketplace">Extension Marketplace</option>
    </select>
  </div>

  {#if source === 'remote'}
    <div class="form-group">
      <label for="url">Extension URL</label>
      <input 
        type="url" 
        id="url" 
        bind:value={url} 
        placeholder="https://example.com/extension.zip"
        required
      />
      <div class="form-help">
        Enter the URL of a ZIP file containing the extension.
      </div>
    </div>
  {:else if source === 'local'}
    <div class="form-group">
      <label for="path">Extension Path</label>
      <input 
        type="text" 
        id="path" 
        bind:value={path} 
        placeholder="/path/to/extension"
        required
      />
      <div class="form-help">
        Enter the local file system path to the extension directory.
      </div>
    </div>
  {:else if source === 'marketplace'}
    <div class="form-group">
      <label for="name">Extension Name</label>
      <input 
        type="text" 
        id="name" 
        bind:value={name} 
        placeholder="awesome-extension"
        required
      />
      <div class="form-help">
        Enter the name of the extension to install from the marketplace.
      </div>
    </div>
    
    <div class="marketplace-note">
      <p>
        <strong>Note:</strong> The Extension Marketplace feature is coming soon. For now, you can install extensions from a URL or local directory.
      </p>
    </div>
  {/if}

  <div class="form-actions">
    <button type="button" class="btn btn-secondary" on:click={handleCancel} disabled={loading}>
      Cancel
    </button>
    <button type="submit" class="btn btn-primary" disabled={loading}>
      {#if loading}
        Installing...
      {:else}
        Install Extension
      {/if}
    </button>
  </div>
</form>

<style>
  .extension-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .form-group label {
    font-weight: 500;
  }

  .form-help {
    font-size: 0.75rem;
    color: #6c757d;
  }

  input, select {
    padding: 0.5rem;
    border: 1px solid #ced4da;
    border-radius: 0.25rem;
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .marketplace-note {
    padding: 1rem;
    background-color: #e2f0fd;
    border-left: 4px solid #007bff;
    border-radius: 0.25rem;
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

  .alert-close {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: inherit;
    padding: 0;
    line-height: 1;
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

  .btn:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }
</style>

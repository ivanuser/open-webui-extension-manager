<!-- Extension Card Component -->
<script>
  import { createEventDispatcher } from 'svelte';

  // Props
  export let extension = {};

  // Event dispatcher
  const dispatch = createEventDispatcher();

  // State
  let showSettings = false;
  let settingsForm = {};

  // Initialize settings form when extension changes
  $: {
    if (extension.settings) {
      settingsForm = extension.settings.reduce((acc, setting) => {
        acc[setting.name] = setting.value ?? setting.default;
        return acc;
      }, {});
    }
  }

  // Handle action button clicks
  function handleAction(action) {
    dispatch('action', {
      name: extension.name,
      action
    });
  }

  // Handle settings form submission
  function handleSettingsSubmit() {
    dispatch('updateSettings', {
      name: extension.name,
      settings: settingsForm
    });
    showSettings = false;
  }

  // Get status color
  function getStatusColor(status) {
    switch (status) {
      case 'active':
        return 'green';
      case 'inactive':
        return 'gray';
      case 'error':
        return 'red';
      case 'pending':
        return 'orange';
      default:
        return 'gray';
    }
  }

  // Format date
  function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch (e) {
      return dateString;
    }
  }
</script>

<div class="extension-card">
  <div class="extension-card__header">
    <div class="extension-card__status" style="background-color: {getStatusColor(extension.status)};"></div>
    <h3 class="extension-card__title">{extension.name}</h3>
    <div class="extension-card__version">v{extension.version}</div>
  </div>

  <div class="extension-card__content">
    <p class="extension-card__description">{extension.description}</p>
    
    <div class="extension-card__meta">
      <div class="extension-card__meta-item">
        <span class="label">Author:</span>
        <span>{extension.author}</span>
      </div>
      
      <div class="extension-card__meta-item">
        <span class="label">Type:</span>
        <span>{extension.type}</span>
      </div>
      
      <div class="extension-card__meta-item">
        <span class="label">Status:</span>
        <span class="status-badge" style="background-color: {getStatusColor(extension.status)};">
          {extension.status}
        </span>
      </div>
      
      {#if extension.installed_at}
        <div class="extension-card__meta-item">
          <span class="label">Installed:</span>
          <span>{formatDate(extension.installed_at)}</span>
        </div>
      {/if}
      
      {#if extension.updated_at}
        <div class="extension-card__meta-item">
          <span class="label">Updated:</span>
          <span>{formatDate(extension.updated_at)}</span>
        </div>
      {/if}
    </div>
    
    {#if extension.dependencies && extension.dependencies.length > 0}
      <div class="extension-card__section">
        <h4>Dependencies</h4>
        <ul class="extension-card__dependencies">
          {#each extension.dependencies as dependency}
            <li>
              {dependency.name}
              {#if dependency.version}
                <span class="dependency-version">v{dependency.version}</span>
              {/if}
              {#if dependency.optional}
                <span class="optional-badge">optional</span>
              {/if}
            </li>
          {/each}
        </ul>
      </div>
    {/if}
    
    {#if extension.error}
      <div class="extension-card__error">
        <h4>Error</h4>
        <pre>{extension.error}</pre>
      </div>
    {/if}
  </div>

  <div class="extension-card__actions">
    {#if extension.status === 'active'}
      <button class="btn btn-secondary" on:click={() => handleAction('disable')}>
        Disable
      </button>
    {:else}
      <button class="btn btn-primary" on:click={() => handleAction('enable')}>
        Enable
      </button>
    {/if}
    
    <button class="btn btn-secondary" on:click={() => showSettings = true}>
      Settings
    </button>
    
    <button class="btn btn-danger" on:click={() => handleAction('uninstall')}>
      Uninstall
    </button>
  </div>

  {#if showSettings}
    <div class="extension-card__settings">
      <div class="settings-header">
        <h4>Settings</h4>
        <button class="settings-close" on:click={() => showSettings = false}>×</button>
      </div>
      
      {#if extension.settings && extension.settings.length > 0}
        <form on:submit|preventDefault={handleSettingsSubmit}>
          {#each extension.settings as setting}
            <div class="form-group">
              <label for={`setting-${setting.name}`}>
                {setting.name}
                {#if setting.required}
                  <span class="required">*</span>
                {/if}
              </label>
              
              {#if setting.description}
                <div class="setting-description">{setting.description}</div>
              {/if}
              
              {#if setting.options}
                <select 
                  id={`setting-${setting.name}`}
                  bind:value={settingsForm[setting.name]}
                  required={setting.required}
                >
                  {#each setting.options as option}
                    <option value={option.value}>{option.label}</option>
                  {/each}
                </select>
              {:else if setting.type === 'boolean'}
                <label class="checkbox-label">
                  <input 
                    type="checkbox" 
                    id={`setting-${setting.name}`}
                    bind:checked={settingsForm[setting.name]}
                  />
                  Enable
                </label>
              {:else if setting.type === 'number'}
                <input 
                  type="number" 
                  id={`setting-${setting.name}`}
                  bind:value={settingsForm[setting.name]}
                  required={setting.required}
                />
              {:else}
                <input 
                  type="text" 
                  id={`setting-${setting.name}`}
                  bind:value={settingsForm[setting.name]}
                  required={setting.required}
                />
              {/if}
            </div>
          {/each}
          
          <div class="form-actions">
            <button type="button" class="btn btn-secondary" on:click={() => showSettings = false}>
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              Save Settings
            </button>
          </div>
        </form>
      {:else}
        <div class="empty-settings">
          <p>This extension has no configurable settings.</p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .extension-card {
    position: relative;
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    background-color: white;
    transition: box-shadow 0.3s ease;
  }

  .extension-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .extension-card__header {
    display: flex;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #eee;
    background-color: #f8f9fa;
  }

  .extension-card__status {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
  }

  .extension-card__title {
    flex: 1;
    margin: 0;
    font-size: 1.25rem;
  }

  .extension-card__version {
    font-size: 0.75rem;
    color: #6c757d;
    padding: 0.25rem 0.5rem;
    background-color: #e9ecef;
    border-radius: 0.25rem;
  }

  .extension-card__content {
    padding: 1rem;
  }

  .extension-card__description {
    margin-top: 0;
    margin-bottom: 1rem;
  }

  .extension-card__meta {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .extension-card__meta-item {
    display: flex;
    flex-direction: column;
  }

  .label {
    font-size: 0.75rem;
    color: #6c757d;
  }

  .status-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    color: white;
    font-size: 0.75rem;
    text-transform: uppercase;
  }

  .extension-card__section {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
  }

  .extension-card__section h4 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }

  .extension-card__dependencies {
    margin: 0;
    padding: 0;
    list-style-type: none;
  }

  .extension-card__dependencies li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
  }

  .dependency-version {
    font-size: 0.75rem;
    color: #6c757d;
  }

  .optional-badge {
    font-size: 0.75rem;
    padding: 0.1rem 0.25rem;
    background-color: #e9ecef;
    border-radius: 0.25rem;
  }

  .extension-card__error {
    margin-top: 1rem;
    padding: 0.5rem;
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 0.25rem;
    color: #721c24;
  }

  .extension-card__error h4 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }

  .extension-card__error pre {
    margin: 0;
    white-space: pre-wrap;
    font-size: 0.75rem;
  }

  .extension-card__actions {
    display: flex;
    gap: 0.5rem;
    padding: 1rem;
    border-top: 1px solid #eee;
    background-color: #f8f9fa;
  }

  .extension-card__settings {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: white;
    z-index: 1;
    padding: 1rem;
    overflow-y: auto;
  }

  .settings-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .settings-header h4 {
    margin: 0;
  }

  .settings-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0;
    line-height: 1;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.25rem;
    font-weight: 500;
  }

  .setting-description {
    font-size: 0.75rem;
    color: #6c757d;
    margin-bottom: 0.25rem;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: normal;
  }

  .required {
    color: #dc3545;
  }

  input, select {
    width: 100%;
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

  .empty-settings {
    text-align: center;
    padding: 2rem;
    color: #6c757d;
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

  .btn-danger {
    background-color: #dc3545;
    color: white;
  }
</style>

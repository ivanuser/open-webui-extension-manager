import ExtensionManager from './ExtensionManager.svelte';
import ExtensionCard from './ExtensionCard.svelte';
import ExtensionForm from './ExtensionForm.svelte';

/**
 * Get UI mount points for the extension manager.
 * @returns {Object} A dictionary mapping mount point names to renderer functions.
 */
export function getMountPoints() {
  return {
    'admin_settings': (container) => {
      return new ExtensionManager({
        target: container
      });
    }
  };
}

export {
  ExtensionManager,
  ExtensionCard,
  ExtensionForm
};

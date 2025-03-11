class Extension(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the extension."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the extension."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the extension does."""
        pass
    
    @property
    @abstractmethod
    def author(self) -> str:
        """The author(s) of the extension."""
        pass
    
    @property
    def dependencies(self) -> List[str]:
        """List of other extensions this extension depends on."""
        return []
    
    @property
    def type(self) -> str:
        """The type of extension (UI, API, Model, Tool, Theme)."""
        return "generic"
    
    @property
    def settings(self) -> Dict[str, Any]:
        """The extension's default settings."""
        return {}
    
    @property
    def static_dir(self) -> Optional[str]:
        """The directory containing static files for this extension."""
        module_dir = os.path.dirname(inspect.getmodule(self).__file__)
        static_path = os.path.join(module_dir, "static")
        return static_path if os.path.exists(static_path) else None
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        """Initialize the extension with the given context."""
        return True
    
    def activate(self) -> bool:
        """Activate the extension."""
        return True
    
    def deactivate(self) -> bool:
        """Deactivate the extension."""
        return True
    
    def uninstall(self) -> bool:
        """Perform cleanup when uninstalling the extension."""
        return True

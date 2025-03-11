C:\Users\ihoner\Documents\src\open-webui-extensions\
│
├── docs/                             # Documentation
│   ├── creating_extensions.md        # Guide for creating extensions
│   ├── extension_api.md              # API reference documentation
│   └── extension_manager.md          # Extension manager usage guide
│
├── example_extension/                # Example extension
│   ├── config/                       # Configuration directory
│   ├── static/                       # Static assets
│   │   └── example.js                # Frontend JavaScript
│   ├── __init__.py                   # Main extension entry point
│   └── api.py                        # API endpoints
│
├── extension_framework/              # Extension framework
│   ├── __init__.py                   # Framework initialization
│   ├── base.py                       # Base extension classes
│   ├── decorators.py                 # Extension decorators
│   ├── hooks.py                      # Hook system
│   └── utils.py                      # Utility functions
│
├── extension_manager/                # Extension manager
│   ├── backend/                      # Backend code
│   │   ├── __init__.py
│   │   ├── api.py                    # API endpoints
│   │   ├── models.py                 # Database models
│   │   └── registry.py               # Extension registry
│   ├── config/                       # Configuration directory
│   ├── frontend/                     # Frontend components
│   │   ├── ExtensionManager.svelte   # Main UI component
│   │   ├── ExtensionCard.svelte      # Extension card component
│   │   └── ExtensionForm.svelte      # Extension form component
│   ├── static/                       # Static assets
│   │   └── extension_manager.js      # Frontend JavaScript
│   └── __init__.py                   # Main extension entry point
│
├── mcp_connector/                    # MCP Connector extension
│   ├── config/                       # Configuration directory
│   ├── static/                       # Static assets
│   │   └── mcp_manager.js            # Frontend JavaScript
│   ├── __init__.py                   # Main extension entry point
│   ├── api.py                        # API endpoints
│   └── mcp_client.py                 # MCP client implementation
│
├── scripts/                          # Installation/utility scripts
│   ├── empty_files/                  # Directory with empty file placeholders
│   │   ├── extension_framework/
│   │   ├── extension_manager/
│   │   ├── example_extension/
│   │   └── mcp_connector/
│   └── install.sh                    # Installation script
│
├── .gitignore                        # Git ignore file
├── LICENSE                           # License file
├── README.md                         # Project readme
├── install.py                        # Python installation script
└── setup.py                          # Package setup for pip

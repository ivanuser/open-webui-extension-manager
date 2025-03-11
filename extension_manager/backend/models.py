from typing import Dict, List, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field
import datetime

class ExtensionStatus(str, Enum):
    """Status of an extension."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"

class ExtensionType(str, Enum):
    """Type of an extension."""
    UI = "ui"
    API = "api"
    MODEL = "model"
    TOOL = "tool"
    THEME = "theme"
    GENERIC = "generic"

class ExtensionSource(str, Enum):
    """Source of an extension."""
    LOCAL = "local"
    REMOTE = "remote"
    MARKETPLACE = "marketplace"
    CUSTOM = "custom"

class ExtensionSetting(BaseModel):
    """A setting for an extension."""
    name: str
    type: str
    default: Any = None
    value: Any = None
    description: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None
    required: bool = False
    category: str = "General"

class ExtensionDependency(BaseModel):
    """A dependency for an extension."""
    name: str
    version: Optional[str] = None
    optional: bool = False

class ExtensionInfo(BaseModel):
    """Information about an extension."""
    name: str
    version: str
    description: str
    author: str
    type: ExtensionType = ExtensionType.GENERIC
    status: ExtensionStatus = ExtensionStatus.INACTIVE
    source: ExtensionSource = ExtensionSource.LOCAL
    path: Optional[str] = None
    url: Optional[str] = None
    dependencies: List[ExtensionDependency] = []
    settings: List[ExtensionSetting] = []
    installed_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    error: Optional[str] = None

class ExtensionAction(BaseModel):
    """An action to perform on an extension."""
    action: str = Field(..., description="The action to perform (enable, disable, update, uninstall)")
    name: str = Field(..., description="The name of the extension")

class ExtensionInstall(BaseModel):
    """Information for installing an extension."""
    source: ExtensionSource = Field(..., description="The source of the extension")
    url: Optional[str] = Field(None, description="The URL of the extension (for remote sources)")
    path: Optional[str] = Field(None, description="The path to the extension (for local sources)")
    name: Optional[str] = Field(None, description="The name of the extension (for marketplace sources)")

class ExtensionSettings(BaseModel):
    """Settings for an extension."""
    name: str = Field(..., description="The name of the extension")
    settings: Dict[str, Any] = Field(..., description="The settings to update")

class ExtensionList(BaseModel):
    """A list of extensions."""
    extensions: List[ExtensionInfo] = []

class ExtensionFilters(BaseModel):
    """Filters for listing extensions."""
    types: Optional[List[ExtensionType]] = None
    status: Optional[List[ExtensionStatus]] = None
    sources: Optional[List[ExtensionSource]] = None
    search: Optional[str] = None

class ExtensionActionResponse(BaseModel):
    """Response for an extension action."""
    success: bool = True
    message: str = ""
    extension: Optional[ExtensionInfo] = None

class ExtensionListResponse(BaseModel):
    """Response for listing extensions."""
    success: bool = True
    message: str = ""
    extensions: List[ExtensionInfo] = []
    total: int = 0
    page: int = 1
    page_size: int = 10
    filters: Optional[ExtensionFilters] = None

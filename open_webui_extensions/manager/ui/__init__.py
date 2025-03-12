from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

ui_router = APIRouter()

@ui_router.get("/", response_class=HTMLResponse)
async def extension_manager_ui(request: Request):
    """Render the extension manager UI."""
    return templates.TemplateResponse("manager.html", {"request": request})

@ui_router.get("/admin-integration.js", response_class=HTMLResponse)
async def admin_integration_js(request: Request):
    """Provide the JavaScript for admin integration."""
    return templates.TemplateResponse("admin-integration.js", {"request": request, "media_type": "application/javascript"})

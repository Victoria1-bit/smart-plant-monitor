from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"active": "dashboard"})


@router.get("/history")
def history_page(request: Request):
    return templates.TemplateResponse(request, "history.html", {"active": "history"})


@router.get("/settings")
def settings_page(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"active": "settings"})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"active": "login"})

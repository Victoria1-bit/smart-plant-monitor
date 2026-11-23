from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models import User
from app.services.auth import current_user

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


def show_page(request: Request, user: User | None, template, active):
    # Pages with plant data are only shown to signed-in users
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request, template, {"active": active, "user": user})


@router.get("/")
def home(request: Request, user: User | None = Depends(current_user)):
    return show_page(request, user, "dashboard.html", "dashboard")


@router.get("/history")
def history_page(request: Request, user: User | None = Depends(current_user)):
    return show_page(request, user, "history.html", "history")


@router.get("/settings")
def settings_page(request: Request, user: User | None = Depends(current_user)):
    return show_page(request, user, "settings.html", "settings")


@router.get("/login")
def login_page(request: Request, user: User | None = Depends(current_user)):
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"active": "login", "user": None})


@router.get("/register")
def register_page(request: Request, user: User | None = Depends(current_user)):
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "register.html", {"active": "login", "user": None})

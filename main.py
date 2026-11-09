from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from pump import MAX_SECONDS
from sensor import get_status
from simulator import build_history, make_reading, next_moisture

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MAX_READINGS = 1000
READING_INTERVAL = 60   # seconds between simulated readings

# Readings are kept in lists for now, newest first. This will be a database later.
readings = build_history()

settings = {
    "dry_threshold": 30,
    "wet_threshold": 70,
    "water_seconds": 3,
    "cooldown_minutes": 60,
    "auto_water": False,
}


class Settings(BaseModel):
    dry_threshold: int = Field(ge=5, le=60)
    wet_threshold: int = Field(ge=40, le=95)
    water_seconds: int = Field(ge=1, le=MAX_SECONDS)
    cooldown_minutes: int = Field(ge=1, le=1440)
    auto_water: bool


def take_reading():
    # Get a (simulated) reading and save it
    reading = make_reading(
        next_moisture(readings[0]["moisture"]),
        dry_threshold=settings["dry_threshold"],
        wet_threshold=settings["wet_threshold"],
    )
    readings.insert(0, reading)
    del readings[MAX_READINGS:]
    return reading


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"active": "dashboard", "max_seconds": MAX_SECONDS})


@app.get("/api/reading")
def get_reading():
    return take_reading()


@app.get("/api/readings")
def get_readings(hours: int | None = None, limit: int = 10):
    # Return readings from the last few hours, or just the latest few
    if hours is None:
        return readings[:limit]
    cutoff = datetime.now() - timedelta(hours=hours)
    return [r for r in readings if datetime.fromisoformat(r["timestamp"]) >= cutoff]


def latest_reading():
    # Pages check often, so only take a new reading once a minute
    age = datetime.now() - datetime.fromisoformat(readings[0]["timestamp"])
    if age.total_seconds() >= READING_INTERVAL:
        return take_reading()
    return readings[0]


@app.get("/api/status")
def get_status_summary():
    return {
        "reading": latest_reading(),
        "sensor_connected": False,
        "settings": settings,
    }


@app.get("/api/settings")
def read_settings():
    return settings


@app.put("/api/settings")
def update_settings(new_settings: Settings):
    if new_settings.dry_threshold >= new_settings.wet_threshold:
        raise HTTPException(400, "The dry level must be lower than the wet level.")

    settings.update(new_settings.model_dump())

    # Saved readings need their status worked out again with the new levels
    for r in readings:
        r["status"] = get_status(r["moisture"], settings["dry_threshold"], settings["wet_threshold"])
    return settings


@app.post("/api/login")
def login():
    # The login form is ready but real accounts are not built yet
    raise HTTPException(501, "Sign in is not connected yet. Accounts will be added with the database.")


@app.get("/history", include_in_schema=False)
def history_page(request: Request):
    return templates.TemplateResponse(request, "history.html", {"active": "history"})


@app.get("/settings", include_in_schema=False)
def settings_page(request: Request):
    return templates.TemplateResponse(
        request, "settings.html", {"active": "settings", "max_seconds": MAX_SECONDS}
    )


@app.get("/login", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"active": "login"})

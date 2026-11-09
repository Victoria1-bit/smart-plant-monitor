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
readings, watering_events = build_history()

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
    auto_water_if_dry(reading)
    return reading


def auto_water_if_dry(reading):
    # Use the same safeguards as manual watering
    if not settings["auto_water"] or reading["moisture"] >= settings["dry_threshold"]:
        return
    minutes = minutes_since_last_watering()
    if minutes is None or minutes >= settings["cooldown_minutes"]:
        record_watering(settings["water_seconds"], "Automatic")


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"active": "dashboard"})


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


class WaterRequest(BaseModel):
    seconds: int = Field(ge=1, le=MAX_SECONDS)


def minutes_since_last_watering():
    if not watering_events:
        return None
    last = datetime.fromisoformat(watering_events[0]["timestamp"])
    return (datetime.now() - last).total_seconds() / 60


def record_watering(seconds, trigger):
    # SIMULATED: this only changes the numbers. It never runs pump.py.
    # A real pump route must wait until the login is finished.
    before = readings[0]["moisture"]
    after = min(100, before + seconds * 4)
    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "trigger": trigger,
        "seconds": seconds,
        "before": before,
        "after": after,
        "simulated": True,
    }
    watering_events.insert(0, event)
    readings.insert(0, make_reading(after, dry_threshold=settings["dry_threshold"],
                                    wet_threshold=settings["wet_threshold"]))
    return event


@app.post("/api/water")
def water_now(request: WaterRequest):
    if readings[0]["moisture"] > settings["wet_threshold"]:
        raise HTTPException(409, "The soil is already wet, so watering was not started.")

    minutes = minutes_since_last_watering()
    if minutes is not None and minutes < settings["cooldown_minutes"]:
        wait = int(settings["cooldown_minutes"] - minutes) + 1
        raise HTTPException(409, f"Watered recently. Try again in {wait} minutes.")

    return record_watering(request.seconds, "Manual")


@app.get("/api/watering")
def get_watering():
    return watering_events


@app.post("/api/login")
def login():
    # The login form is ready but real accounts are not built yet
    raise HTTPException(501, "Sign in is not connected yet. Accounts will be added with the database.")


@app.get("/history", include_in_schema=False)
def history_page(request: Request):
    return templates.TemplateResponse(request, "history.html", {"active": "history"})

from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from simulator import build_history, make_reading, next_moisture

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MAX_READINGS = 1000

# Readings are kept in lists for now, newest first. This will be a database later.
readings, watering_events = build_history()


def take_reading():
    # Get a (simulated) reading and save it
    reading = make_reading(next_moisture(readings[0]["moisture"]))
    readings.insert(0, reading)
    del readings[MAX_READINGS:]
    return reading


@app.get("/", include_in_schema=False)
def home(request: Request):
    reading = take_reading()
    return templates.TemplateResponse(
        request, "dashboard.html", {"reading": reading, "readings": readings[:10]}
    )


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

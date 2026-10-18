"""
Smart Plant Monitor - FastAPI application (Week 5 starter).

Run it with:
    fastapi dev main.py

Then open http://127.0.0.1:8000 for the dashboard
or http://127.0.0.1:8000/docs for the API documentation.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import DRY_THRESHOLD, WET_THRESHOLD
from plant import get_plant_status, get_status_message
from schemas import ReadingResponse
from simulator import get_simulated_reading

app = FastAPI(title="Smart Plant Monitor")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Recent readings are kept in memory for now.
# Later this will be replaced by the database.
readings = []
MAX_READINGS = 20


def take_reading():
    """Take one (simulated) reading, add the plant status and save it.

    When the real sensor is ready, only the first line needs to change
    (to call hardware/sensor.py instead of the simulator).
    """
    reading = get_simulated_reading()
    status = get_plant_status(reading["moisture_percent"])
    reading["status"] = status
    reading["message"] = get_status_message(status)

    readings.append(reading)
    if len(readings) > MAX_READINGS:
        readings.pop(0)          # forget the oldest reading

    return reading


# ---------- Web pages ----------

@app.get("/", include_in_schema=False)
def home(request: Request):
    """Show the dashboard with the latest reading and recent history."""
    latest = take_reading()
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "title": "Dashboard",
            "latest": latest,
            "history": list(reversed(readings)),   # newest first
            "dry_threshold": DRY_THRESHOLD,
            "wet_threshold": WET_THRESHOLD,
        },
    )


# ---------- API ----------

@app.get("/api/readings/latest", response_model=ReadingResponse)
def get_latest_reading():
    """Take a new reading and return it as JSON."""
    return take_reading()


@app.get("/api/readings", response_model=list[ReadingResponse])
def get_readings():
    """Return the recent readings, newest first."""
    return list(reversed(readings))


@app.get("/api/health")
def health_check():
    """Simple check that the app is running (useful later on AWS)."""
    return {"status": "ok"}


# NOTE: There is deliberately NO pump endpoint yet.
# Turning on a water pump from the internet must require a login,
# so it will be added together with authentication in a later week.

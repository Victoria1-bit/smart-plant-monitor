from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sensor import read_moisture, get_status

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Readings are kept in a list for now. This will be a database later.
readings = []


def take_reading():
    # Get a (simulated) reading, work out the status and save it
    moisture = read_moisture()
    reading = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "moisture": moisture,
        "status": get_status(moisture),
        "simulated": True,
    }
    readings.insert(0, reading)   # newest first
    del readings[10:]             # only keep the last 10
    return reading


@app.get("/", include_in_schema=False)
def home(request: Request):
    reading = take_reading()
    return templates.TemplateResponse(
        request, "dashboard.html", {"reading": reading, "readings": readings}
    )


@app.get("/api/reading")
def get_reading():
    return take_reading()


@app.get("/api/readings")
def get_readings():
    return readings

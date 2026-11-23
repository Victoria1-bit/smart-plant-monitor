from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import readings as reading_service

router = APIRouter(
    prefix="/api",
    tags=["readings"],
)


@router.get("/reading")
def get_reading(db: Session = Depends(get_db)):
    # Take a new (simulated) reading, save it and return it
    levels = reading_service.get_levels(db)
    reading = reading_service.take_simulated_reading(db)
    return reading_service.reading_to_dict(reading, levels)


@router.get("/readings")
def get_readings(hours: int | None = None, limit: int = 10, db: Session = Depends(get_db)):
    # Return readings from the last few hours, or just the latest few
    levels = reading_service.get_levels(db)
    if hours is None:
        found = reading_service.recent_readings(db, limit)
    else:
        found = reading_service.readings_since(db, hours)
    return [reading_service.reading_to_dict(r, levels) for r in found]


@router.get("/status")
def get_status_summary(db: Session = Depends(get_db)):
    levels = reading_service.get_levels(db)
    reading = reading_service.latest_reading(db)

    # The light comes on when the soil is dry. SIMULATED: the page shows
    # what the light should be doing, as no real light is connected yet.
    light = "On" if reading.moisture < levels.dry_threshold else "Off"

    return {
        "reading": reading_service.reading_to_dict(reading, levels),
        "light": light,
        "sensor_connected": False,
        "settings": {"dry_threshold": levels.dry_threshold, "wet_threshold": levels.wet_threshold},
    }

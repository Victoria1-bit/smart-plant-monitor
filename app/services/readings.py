# Saving and loading soil moisture readings.

import random
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Reading, Setting

READING_INTERVAL = 60   # seconds between simulated readings
WATER_BELOW = 27        # someone waters the simulated plant by hand below this level
WATERED_LEVEL = 68      # and it goes back up to this level


def get_status(moisture, dry_threshold, wet_threshold):
    # Turn a moisture percentage into dry, normal or wet
    if moisture < dry_threshold:
        return "Dry"
    elif moisture > wet_threshold:
        return "Wet"
    else:
        return "Normal"


def get_levels(db: Session):
    # The moisture levels are kept in one row. Make it the first time.
    levels = db.get(Setting, 1)
    if levels is None:
        levels = Setting(setting_id=1, dry_threshold=30, wet_threshold=70)
        db.add(levels)
        db.commit()
    return levels


def reading_to_dict(reading: Reading, levels: Setting):
    # The format the pages expect. The status is worked out from the
    # current levels, so changing the levels changes it straight away.
    return {
        "time": reading.recorded_at.strftime("%H:%M:%S"),
        "timestamp": reading.recorded_at.isoformat(timespec="seconds"),
        "moisture": reading.moisture,
        "status": get_status(reading.moisture, levels.dry_threshold, levels.wet_threshold),
        "simulated": reading.simulated,
    }


def save_reading(db: Session, moisture, simulated=True, when=None):
    reading = Reading(moisture=moisture, simulated=simulated, recorded_at=when or datetime.now())
    db.add(reading)
    db.commit()
    return reading


def newest_reading(db: Session):
    return db.scalars(select(Reading).order_by(Reading.recorded_at.desc()).limit(1)).first()


def recent_readings(db: Session, limit=10):
    return db.scalars(select(Reading).order_by(Reading.recorded_at.desc()).limit(limit)).all()


def readings_since(db: Session, hours):
    cutoff = datetime.now() - timedelta(hours=hours)
    return db.scalars(
        select(Reading).where(Reading.recorded_at >= cutoff).order_by(Reading.recorded_at.desc())
    ).all()


# SIMULATED readings. There is no real sensor connected yet, so these
# make believable values for the pages to show. Every one is saved with
# simulated = True. This part goes when real readings arrive over MQTT.

def next_moisture(last):
    # Move a small amount from the last reading, drying out slowly
    return max(0, min(100, last + random.choice([-1, -1, 0, 0, 1])))


def take_simulated_reading(db: Session):
    last = newest_reading(db)
    moisture = next_moisture(last.moisture if last else 60)
    return save_reading(db, moisture, simulated=True)


def latest_reading(db: Session):
    # Pages check often, so only take a new reading once a minute
    last = newest_reading(db)
    if last is None or (datetime.now() - last.recorded_at).total_seconds() >= READING_INTERVAL:
        return take_simulated_reading(db)
    return last


def add_simulated_history(db: Session, days=7):
    # Fill an empty database with one reading per hour for the last few days
    if newest_reading(db) is not None:
        return

    now = datetime.now()
    moisture = 60
    for hours_ago in range(days * 24, 0, -1):
        moisture -= random.randint(0, 1)
        if moisture < WATER_BELOW:
            moisture = WATERED_LEVEL
        db.add(Reading(moisture=moisture, simulated=True, recorded_at=now - timedelta(hours=hours_ago)))
    db.commit()

# Simulated soil moisture data.
#
# There is no real sensor connected yet. This file makes believable
# readings so the web pages have something to show. Every reading is
# marked as simulated. Delete this file when real readings arrive over
# MQTT.

import random
from datetime import datetime, timedelta

from sensor import get_status

WATER_BELOW = 27      # someone waters the simulated plant by hand below this level
WATERED_LEVEL = 68    # and it goes back up to this level


def make_reading(moisture, when=None, dry_threshold=30, wet_threshold=70):
    # Build one reading in the format the API returns
    when = when or datetime.now()
    return {
        "time": when.strftime("%H:%M:%S"),
        "timestamp": when.isoformat(timespec="seconds"),
        "moisture": moisture,
        "status": get_status(moisture, dry_threshold, wet_threshold),
        "simulated": True,
    }


def next_moisture(last):
    # Move a small amount from the last reading, drying out slowly
    return max(0, min(100, last + random.choice([-1, -1, 0, 0, 1])))


def build_history(days=7):
    # Make one reading per hour for the last few days, newest first
    now = datetime.now()
    moisture = 60
    readings = []

    for hours_ago in range(days * 24, 0, -1):
        when = now - timedelta(hours=hours_ago)
        moisture -= random.randint(0, 1)

        if moisture < WATER_BELOW:
            moisture = WATERED_LEVEL

        readings.insert(0, make_reading(moisture, when))

    return readings

"""
Plant logic: turn a moisture percentage into a plant status.

This file has no hardware code, so it works the same with simulated
readings and with the real sensor.
"""

from config import DRY_THRESHOLD, WET_THRESHOLD, SENSOR_RAW_DRY, SENSOR_RAW_WET


def raw_to_percent(raw_value):
    """Convert a raw MCP3008 value (0-1023) into a moisture percentage (0-100).

    A capacitive sensor reads high when dry and low when wet, so the
    scale is flipped: SENSOR_RAW_DRY becomes 0% and SENSOR_RAW_WET becomes 100%.
    """
    percent = (SENSOR_RAW_DRY - raw_value) / (SENSOR_RAW_DRY - SENSOR_RAW_WET) * 100
    # Keep the result between 0 and 100 in case the reading is outside calibration
    percent = max(0, min(100, percent))
    return round(percent, 1)


def get_plant_status(moisture_percent):
    """Return 'dry', 'normal' or 'wet' for a moisture percentage."""
    if moisture_percent < DRY_THRESHOLD:
        return "dry"
    elif moisture_percent > WET_THRESHOLD:
        return "wet"
    else:
        return "normal"


def get_status_message(status):
    """Return a short, friendly message to show on the dashboard."""
    messages = {
        "dry": "Soil is dry. The plant needs water.",
        "normal": "Soil moisture is in a healthy range.",
        "wet": "Soil is very wet. Do not water.",
    }
    return messages[status]

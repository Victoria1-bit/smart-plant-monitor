"""
SIMULATED soil moisture sensor.

There is no real sensor connected yet. This module makes up raw
readings that behave like a real capacitive sensor in a plant pot:
the soil slowly dries out, with a little random noise.

Every reading returned from here is marked "simulated": True so it can
never be mistaken for real data.
"""

import random
from datetime import datetime

from plant import raw_to_percent

# Start somewhere in the "normal" range
_current_raw = 550


def read_simulated_raw():
    """Return a fake raw MCP3008 value (0-1023).

    Each call the soil gets a tiny bit drier (the raw value goes up).
    When it gets very dry we pretend the plant was watered.
    """
    global _current_raw

    _current_raw += random.randint(-3, 12)   # mostly drying out, a little noise

    if _current_raw > 820:                   # very dry -> pretend someone watered it
        _current_raw = 380

    _current_raw = max(0, min(1023, _current_raw))
    return _current_raw


def get_simulated_reading():
    """Return one simulated reading as a dictionary."""
    raw = read_simulated_raw()
    return {
        "raw_value": raw,
        "moisture_percent": raw_to_percent(raw),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "simulated": True,
    }

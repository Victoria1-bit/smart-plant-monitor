"""
STARTER MODULE - real soil moisture sensor (NOT TESTED YET).

Hardware: capacitive soil moisture sensor -> MCP3008 channel 0 -> Pi 5 SPI0.
See docs/wiring-plan.md for the wiring.

Why gpiozero? The old RPi.GPIO library does not work on the Raspberry Pi 5.
gpiozero comes with Raspberry Pi OS and has a ready-made MCP3008 class.

Before this will work on the Pi:
    1. Enable SPI:  sudo raspi-config -> Interface Options -> SPI -> Yes
    2. Install:     pip install -r requirements-pi.txt
"""

from datetime import datetime

from plant import raw_to_percent

SENSOR_CHANNEL = 0   # MCP3008 input CH0


def read_raw():
    """Read the sensor through the MCP3008 and return a value from 0 to 1023."""
    # Imported here so the rest of the project still runs on a laptop,
    # where gpiozero and the SPI hardware are not available.
    from gpiozero import MCP3008

    adc = MCP3008(channel=SENSOR_CHANNEL)
    raw = round(adc.value * 1023)    # gpiozero gives 0.0-1.0, we want 0-1023
    adc.close()
    return raw


def get_sensor_reading():
    """Return one real reading in the same format as simulator.py."""
    raw = read_raw()
    return {
        "raw_value": raw,
        "moisture_percent": raw_to_percent(raw),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "simulated": False,
    }


if __name__ == "__main__":
    # Quick test on the Pi:  python -m hardware.sensor
    # Use this to find SENSOR_RAW_DRY (sensor in air) and SENSOR_RAW_WET (in water).
    print(get_sensor_reading())

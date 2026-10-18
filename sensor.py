# Soil moisture sensor.
#
# There is no real sensor connected yet, so read_moisture() returns a
# SIMULATED value. read_real_sensor() is for later, on the Raspberry Pi 5,
# and has not been tested.

import random

# Raw MCP3008 values for our sensor (0 to 1023).
# These are guesses until we measure the real sensor in air and in water.
RAW_DRY = 800
RAW_WET = 350


def read_moisture():
    # Simulated reading: a random moisture percentage
    return random.randint(10, 90)


def read_real_sensor():
    # Read the capacitive sensor through the MCP3008 on channel 0.
    # gpiozero is used because RPi.GPIO does not work on the Pi 5.
    # Only works on the Pi with SPI turned on. NOT TESTED YET.
    from gpiozero import MCP3008

    adc = MCP3008(channel=0)
    raw = adc.value * 1023
    adc.close()

    # The sensor gives a higher number when the soil is drier,
    # so we flip it to get a percentage
    percent = (RAW_DRY - raw) / (RAW_DRY - RAW_WET) * 100
    percent = max(0, min(100, percent))
    return round(percent)


def get_status(moisture):
    # Turn a moisture percentage into dry, normal or wet
    if moisture < 30:
        return "Dry"
    elif moisture > 70:
        return "Wet"
    else:
        return "Normal"

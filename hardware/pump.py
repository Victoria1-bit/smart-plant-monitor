# Water pump control. NOT TESTED YET.
#
# The pump is switched by a MOSFET connected to GPIO17 (pin 11).
# The pump has its own 5V supply, never the Pi's 5V pin.
# There is no web route for the pump until we add a login.

from time import sleep

PUMP_PIN = 17
MAX_SECONDS = 5


def water_plant(seconds):
    # Run the pump for a few seconds, never longer than MAX_SECONDS
    from gpiozero import OutputDevice

    seconds = min(seconds, MAX_SECONDS)
    pump = OutputDevice(PUMP_PIN)

    pump.on()
    sleep(seconds)
    pump.off()
    pump.close()

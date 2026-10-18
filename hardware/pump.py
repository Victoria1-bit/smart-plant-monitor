"""
STARTER MODULE - water pump control (NOT TESTED YET).

Hardware: 5V mini water pump switched by a logic-level MOSFET module
on GPIO17 (physical pin 11). The pump has its OWN 5V supply - never
power it from the Pi's 5V pin. See docs/wiring-plan.md.

Safety:
    - The pump always turns itself off after PUMP_MAX_SECONDS.
    - There is no web endpoint for the pump yet. It will only be added
      once the dashboard has a login.
"""

from time import sleep

from config import PUMP_GPIO_PIN, PUMP_MAX_SECONDS


def run_pump(seconds):
    """Turn the pump on for a number of seconds, then turn it off.

    The time is limited to PUMP_MAX_SECONDS so a mistake can never
    flood the plant.
    """
    from gpiozero import OutputDevice   # only available on the Pi

    seconds = max(0, min(seconds, PUMP_MAX_SECONDS))
    pump = OutputDevice(PUMP_GPIO_PIN, active_high=True, initial_value=False)

    try:
        print(f"Pump ON for {seconds} seconds")
        pump.on()
        sleep(seconds)
    finally:
        pump.off()        # 'finally' makes sure the pump stops even if there is an error
        pump.close()
        print("Pump OFF")


if __name__ == "__main__":
    # Quick test on the Pi (with the pump tube in a cup of water):
    #   python -m hardware.pump
    run_pump(2)

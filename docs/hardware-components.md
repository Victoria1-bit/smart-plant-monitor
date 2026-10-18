# Hardware Component List

| # | Component | Qty | Purpose | Notes |
|---|---|---|---|---|
| 1 | Raspberry Pi 5 (4GB or 8GB) | 1 | Main controller: reads the sensor, controls the pump, sends MQTT messages | Runs Raspberry Pi OS (64-bit) |
| 2 | Official Raspberry Pi 5 27W USB-C power supply | 1 | Powers the Pi | The Pi 5 needs 5V 5A for full USB power |
| 3 | microSD card (32GB+) | 1 | Operating system | |
| 4 | Capacitive soil moisture sensor (v1.2 or v2.0) | 1 | Measures soil moisture | Capacitive, not resistive: it does not corrode in the soil. Power it from **3.3V** so its output never goes above 3.3V |
| 5 | MCP3008 8-channel 10-bit ADC (DIP-16) | 1 | Converts the sensor's analog voltage into a number (0–1023) | The Pi 5 has no analog inputs, so this is required. Talks to the Pi over SPI |
| 6 | 3–5V mini submersible water pump | 1 | Waters the plant | Usually draws 100–200 mA, too much for a GPIO pin |
| 7 | Logic-level N-channel MOSFET module (e.g. IRLZ44N or IRF520-style module rated for 3.3V logic) | 1 | Lets the Pi's 3.3V GPIO pin switch the pump's 5V supply | Alternative: 5V relay module with a 3.3V-compatible input. A MOSFET is quieter and smaller |
| 8 | 1N4007 (or 1N5819) diode | 1 | Flyback protection across the pump motor | Skip if the MOSFET module already has one built in |
| 9 | 220 Ω resistor | 1 | Gate resistor between GPIO17 and the MOSFET | Not needed if using a module that includes it |
| 10 | 10 kΩ resistor | 1 | Pull-down on the MOSFET gate so the pump stays OFF while the Pi boots | Not needed if using a module that includes it |
| 11 | Separate 5V supply for the pump (USB breakout or 4×AA pack) | 1 | Powers the pump | **Do not** power the pump from the Pi's 5V pin |
| 12 | Half-size or full-size breadboard | 1 | Prototyping | |
| 13 | Jumper wires (male-male, male-female) | ~20 | Connections | |
| 14 | Silicone tubing (to fit the pump outlet) | ~1 m | Carries water to the pot | |
| 15 | Small water container | 1 | Reservoir for the pump | |
| 16 | GPIO ribbon cable + T-cobbler (optional) | 1 | Makes breadboard wiring easier and safer | |

## Why these parts

- **Capacitive sensor:** cheap resistive sensors corrode within weeks because current flows through the soil. Capacitive sensors are sealed.
- **MCP3008:** the Pi 5 can only read digital signals. The sensor gives a voltage between 0 and about 3V, so an ADC is needed. The MCP3008 is widely used in Raspberry Pi tutorials and `gpiozero` supports it directly.
- **MOSFET driver:** a GPIO pin can only safely supply a few milliamps at 3.3V. The pump needs much more current at 5V, so the GPIO pin switches the MOSFET and the MOSFET switches the pump.

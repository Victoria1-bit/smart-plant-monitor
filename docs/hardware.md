# Hardware

## Components

| Component | Qty | Purpose |
|---|---|---|
| Raspberry Pi 5 and official 27W power supply | 1 | Main controller |
| microSD card, 32GB | 1 | Raspberry Pi OS |
| Capacitive soil moisture sensor (v1.2 or v2.0) | 1 | Measures soil moisture. Capacitive sensors don't corrode like resistive ones |
| MCP3008 ADC | 1 | The Pi 5 has no analog inputs, so this converts the sensor voltage to a number |
| 3-5V mini submersible water pump | 1 | Waters the plant |
| Logic-level MOSFET module (e.g. IRLZ44N) | 1 | Lets a 3.3V GPIO pin switch the 5V pump |
| 1N4007 diode | 1 | Protects the circuit from the pump motor (skip if the module has one) |
| 220 Ω and 10 kΩ resistors | 1 each | Gate resistor and pull-down (skip if the module has them) |
| Separate 5V supply for the pump | 1 | The pump must not run from the Pi's 5V pin |
| Breadboard, jumper wires, tubing, water container | - | Building the prototype |

## Wiring plan

This is a plan for drawing the Fritzing diagram. It has not been built
or tested yet, and there is no Fritzing file yet.

Pin numbers are the physical pins on the Pi's 40-pin header.

### MCP3008 to Raspberry Pi 5

| MCP3008 pin | Connect to |
|---|---|
| 16 VDD | 3.3V (Pi pin 1) |
| 15 VREF | 3.3V (Pi pin 1) |
| 14 AGND | GND (Pi pin 6) |
| 13 CLK | Pi pin 23 (GPIO11) |
| 12 DOUT | Pi pin 21 (GPIO9) |
| 11 DIN | Pi pin 19 (GPIO10) |
| 10 CS | Pi pin 24 (GPIO8) |
| 9 DGND | GND (Pi pin 6) |
| 1 CH0 | Sensor AOUT |

### Soil sensor

| Sensor pin | Connect to |
|---|---|
| VCC | 3.3V |
| GND | GND |
| AOUT | MCP3008 pin 1 (CH0) |

### Pump and MOSFET

| From | To |
|---|---|
| Pi pin 11 (GPIO17) | 220 Ω resistor, then MOSFET gate |
| MOSFET gate | 10 kΩ resistor to GND |
| MOSFET source | GND |
| Pump supply + | Pump + |
| Pump - | MOSFET drain |
| Pump supply - | GND (shared with the Pi) |
| 1N4007 diode | Across the pump, stripe side to pump + |

### Before powering on

- Turn on SPI: `sudo raspi-config`, then Interface Options, then SPI
- Check the pump is not connected to the Pi's 5V pin
- Check the pump supply ground is joined to the Pi ground
- Keep water away from the breadboard

# Hardware Wiring Plan (for the Fritzing diagram)

> **Status:** this is a plan only. It has **not** been built or tested,
> and **no Fritzing (.fzz) file has been created yet**. Use these tables
> to draw the breadboard view in Fritzing.

Pin numbers below are **physical header pins** on the Raspberry Pi 5
(pin 1 is the 3.3V pin nearest the SD card end). The Pi 5 uses the same
40-pin layout as earlier models.

## 1. Power rails on the breadboard

| From | To | Wire colour (suggested) |
|---|---|---|
| Pi pin 1 (3.3V) | Breadboard **+ rail (3.3V)** | Red |
| Pi pin 6 (GND) | Breadboard **− rail (GND)** | Black |

## 2. MCP3008 ADC → Raspberry Pi 5 (SPI0)

Place the MCP3008 across the middle gap of the breadboard. Pin 1 is next to the notch/dot.

| MCP3008 pin | Name | Connects to | Pi GPIO |
|---|---|---|---|
| 16 | VDD | 3.3V rail | — |
| 15 | VREF | 3.3V rail | — |
| 14 | AGND | GND rail | — |
| 13 | CLK | Pi pin 23 | GPIO11 (SPI0 SCLK) |
| 12 | DOUT | Pi pin 21 | GPIO9 (SPI0 MISO) |
| 11 | DIN | Pi pin 19 | GPIO10 (SPI0 MOSI) |
| 10 | CS/SHDN | Pi pin 24 | GPIO8 (SPI0 CE0) |
| 9 | DGND | GND rail | — |
| 1 | CH0 | Soil sensor **AOUT** | — |
| 2–8 | CH1–CH7 | Not used (spare for more sensors) | — |

## 3. Capacitive soil moisture sensor

| Sensor pin | Connects to |
|---|---|
| VCC | 3.3V rail |
| GND | GND rail |
| AOUT | MCP3008 pin 1 (CH0) |

Powering it from 3.3V keeps the output below the MCP3008's 3.3V reference.

## 4. Pump and MOSFET driver

The pump uses its **own 5V supply**. Only the grounds are joined.

| From | To | Notes |
|---|---|---|
| Pi pin 11 (GPIO17) | 220 Ω resistor → MOSFET **Gate** (or module **SIG/IN**) | Control signal |
| MOSFET Gate | 10 kΩ resistor → GND | Keeps the pump off during boot |
| MOSFET **Source** (or module GND) | GND rail | |
| External 5V supply **−** | GND rail | **Common ground with the Pi** |
| External 5V supply **+** | Pump **+** (red) | |
| Pump **−** (black) | MOSFET **Drain** (or module V−/OUT−) | MOSFET switches the low side |
| 1N4007 diode | Across the pump: **stripe (cathode) to pump +**, anode to pump − | Flyback protection |

## 5. Pi 5 pins used (summary)

| Physical pin | Function | Used for |
|---|---|---|
| 1 | 3.3V | Sensor + MCP3008 power |
| 6 | GND | Common ground |
| 11 | GPIO17 | Pump MOSFET gate |
| 19 | GPIO10 / MOSI | MCP3008 DIN |
| 21 | GPIO9 / MISO | MCP3008 DOUT |
| 23 | GPIO11 / SCLK | MCP3008 CLK |
| 24 | GPIO8 / CE0 | MCP3008 CS |

## 6. Safety checklist before powering on

- [ ] SPI enabled (`sudo raspi-config` → Interface Options → SPI)
- [ ] The pump is **not** connected to any Pi 5V pin
- [ ] Pump supply ground is joined to the Pi ground
- [ ] Flyback diode is the right way round (stripe to +)
- [ ] Sensor is powered from 3.3V, not 5V
- [ ] Water and the breadboard are kept apart

## 7. Fritzing tips

- Search the Fritzing parts bin for **"MCP3008"**, **"Raspberry Pi"** and **"N-channel MOSFET"**. If there is no Pi 5 part, the Raspberry Pi 4 part has the same 40-pin header and can be used with a note on the diagram.
- A capacitive sensor part is often missing. A generic 3-pin "sensor" part, labelled VCC / GND / AOUT, is fine.
- Use the wire colours above so the breadboard view matches this document.

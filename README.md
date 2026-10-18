# Smart Plant Monitor

A Raspberry Pi 5 system that checks the soil moisture of a plant, shows it
on a web page and waters the plant with a small pump when it is dry.

Repository: _link to be added_

## Concept

Plants are often watered too much or too little. A capacitive soil
moisture sensor in the pot is read by a Raspberry Pi 5. The Pi sends the
readings over MQTT to a FastAPI web app, which saves them in a database
and shows whether the soil is dry, normal or wet. When the soil is dry, a
pump can water the plant. The app will be hosted on AWS with a custom
HTTPS domain.

## Objectives

1. Read soil moisture on a Raspberry Pi 5 using a capacitive sensor and an MCP3008.
2. Show the plant as dry, normal or wet.
3. Send readings from the Pi to the app using MQTT.
4. Save readings in a database.
5. Show the readings on a FastAPI dashboard.
6. Control a water pump safely, only for logged-in users.
7. Deploy the app on AWS with HTTPS and a custom domain.

## Hardware

Raspberry Pi 5, capacitive soil moisture sensor, MCP3008 ADC, mini water
pump, logic-level MOSFET module, diode, separate 5V pump supply,
breadboard and wires.

The full component list and wiring plan are in [docs/hardware.md](docs/hardware.md).
The system diagram is in [docs/architecture.md](docs/architecture.md).

## Files

```
main.py            FastAPI app
sensor.py          Soil moisture readings (simulated for now)
pump.py            Pump control (not tested)
mqtt_client.py     MQTT publish and subscribe (not tested)
templates/         Dashboard page
static/            Stylesheet
docs/              Architecture and hardware
```

## Running the app

First time:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then:

```
source .venv/bin/activate
fastapi dev main.py
```

Open http://127.0.0.1:8000 for the dashboard and http://127.0.0.1:8000/docs
for the API.

## Routes

| Route | What it does |
|---|---|
| `/` | Dashboard |
| `/api/reading` | Takes a new reading and returns it as JSON |
| `/api/readings` | Returns the last 10 readings |

## Progress (Week 5)

Done:
- FastAPI app and dashboard
- Simulated readings, labelled as simulated
- Dry, normal and wet status
- Hardware list, wiring plan and architecture diagram

Not done yet:
- Fritzing diagram
- Testing the sensor and pump on the Pi
- MQTT broker
- Database
- Login
- AWS deployment

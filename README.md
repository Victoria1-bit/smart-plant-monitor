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
main.py            FastAPI app, pages and API
simulator.py       Simulated readings and watering history
sensor.py          Soil moisture readings and dry/normal/wet status
pump.py            Pump control (not tested, not used by the web app)
mqtt_client.py     MQTT publish and subscribe (not tested)
templates/         One HTML page each, sharing base.html
static/            Stylesheet, font, and one JavaScript file per page
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

## Pages

| Page | What it does |
|---|---|
| `/` | Current moisture, watering control and a 24 hour chart |
| `/history` | Chart and table by time range and status, with a CSV download |
| `/watering` | Every watering and what started it |
| `/settings` | Dry and wet levels, watering time, cooldown and automatic watering |
| `/login` | Sign in form. Accounts are not connected yet |

## API

| Route | What it does |
|---|---|
| `GET /api/status` | Latest reading and settings |
| `GET /api/reading` | Takes a new reading and returns it |
| `GET /api/readings` | Latest readings, or `?hours=24` for a time range |
| `POST /api/water` | Simulated watering, with cooldown and wet-soil checks |
| `GET /api/watering` | Watering history |
| `GET`, `PUT /api/settings` | Read or change the settings |
| `POST /api/login` | Returns 501 until accounts exist |

All data is simulated and kept in memory, so it resets when the app
restarts. `POST /api/water` never runs the pump: `pump.py` must stay
unreachable from the web until the login is finished.

The look follows MyControl: the same palette, Space Grotesk font, line
icon style and bottom navigation on phones.

## Progress (Week 5)

Done:
- FastAPI app and web pages: dashboard, history, watering log, settings and sign in form
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

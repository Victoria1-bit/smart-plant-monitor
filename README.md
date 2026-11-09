# Smart Plant Monitor

A Raspberry Pi 5 system that checks the soil moisture of a plant, shows it
on a web page and turns on a light when the soil is too dry.

Repository: _link to be added_

## Concept

Plants are often watered too much or too little. A capacitive soil
moisture sensor in the pot is read by a Raspberry Pi 5. The Pi sends the
readings over MQTT to a FastAPI web app, which saves them in a database
and shows whether the soil is dry, normal or wet. When the soil is dry, a
light comes on. The app will be hosted on AWS with a custom
HTTPS domain.

## Objectives

1. Read soil moisture on a Raspberry Pi 5 using a capacitive sensor and an MCP3008.
2. Show the plant as dry, normal or wet.
3. Send readings from the Pi to the app using MQTT.
4. Save readings in a database.
5. Show the readings on a FastAPI dashboard.
6. Turn on a light when the soil moisture is low.
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
simulator.py       Simulated readings
sensor.py          Soil moisture readings and dry/normal/wet status
pump.py            Left from the earlier watering design (not used)
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
| `/` | Current moisture, low moisture light and a 24 hour chart |
| `/history` | Chart and table by time range and status, with a CSV download |
| `/settings` | Dry and wet levels. The light comes on below the dry level |
| `/login` | Sign in form. Accounts are not connected yet |

## API

| Route | What it does |
|---|---|
| `GET /api/status` | Latest reading, light state and settings |
| `GET /api/reading` | Takes a new reading and returns it |
| `GET /api/readings` | Latest readings, or `?hours=24` for a time range |
| `GET`, `PUT /api/settings` | Read or change the settings |
| `POST /api/login` | Returns 501 until accounts exist |

All data is simulated and kept in memory, so it resets when the app
restarts. The light shown on the dashboard is not a real light yet.

The look follows MyControl: the same palette, Space Grotesk font, line
icon style and bottom navigation on phones.

## Progress (Week 5)

Done:
- FastAPI app and web pages: dashboard, history, settings and sign in form
- Simulated readings, labelled as simulated
- Dry, normal and wet status
- Hardware list, wiring plan and architecture diagram

Not done yet:
- Fritzing diagram
- Testing the sensor and light on the Pi
- MQTT broker
- Database
- Login
- AWS deployment

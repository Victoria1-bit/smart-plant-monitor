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
app/
  main.py            Starts the app, sessions and database tables
  config.py          Settings read from .env
  database.py        Database connection
  models/            Tables: user, reading, setting
  routers/           Pages, readings, settings and sign in routes
  services/          Readings (with the simulator) and passwords
  mqtt_service.py    MQTT publish and subscribe (not tested)
  create_dev_user.py Makes one account for local use
  templates/         One HTML page each, sharing base.html
  static/            Stylesheet, font, and one JavaScript file per page
hardware/
  sensor.py          Sensor reading for the Pi (not tested)
  pump.py            Left from the earlier watering design (not used)
tests/               Database and sign in tests
database_setup.sql   Tables for MySQL
docs/                Architecture and hardware
```

## Running the app

First time:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and set `SECRET_KEY` to a long random value. The file shows
how to make one. `DATABASE_URL` is set to a SQLite file, which needs
nothing else installed. For MySQL, use the second example in the file.

Then:

```
source .venv/bin/activate
fastapi dev app/main.py
```

Open http://127.0.0.1:8000, create an account and sign in.
The API is listed at http://127.0.0.1:8000/docs.

To run the tests:

```
pip install -r requirements-dev.txt
python -m pytest tests
```

## Pages

| Page | What it does |
|---|---|
| `/` | Current moisture, low moisture light and a 24 hour chart |
| `/history` | Chart and table by time range and status, with a CSV download |
| `/settings` | Dry and wet levels. The light comes on below the dry level |
| `/login` | Sign in |
| `/register` | Create an account |

The first three pages send you to `/login` until you sign in.

## API

| Route | What it does |
|---|---|
| `POST /api/auth/register` | Create an account and sign in |
| `POST /api/auth/login` | Sign in |
| `POST /api/auth/logout` | Sign out |
| `GET /api/auth/me` | The signed-in user |
| `GET /api/status` | Latest reading, light state and settings |
| `GET /api/reading` | Takes a new reading, saves it and returns it |
| `GET /api/readings` | Latest readings, or `?hours=24` for a time range |
| `GET`, `PUT /api/settings` | Read or change the settings |

Every route except register and login needs a signed-in user.

## Database

Readings, settings and accounts are saved in a database, so they are
still there after the app restarts.

| Table | What it holds |
|---|---|
| `user` | Name, email and password hash (Argon2). Passwords are never stored |
| `reading` | Moisture percentage, time, and whether it was simulated |
| `setting` | One row with the dry and wet levels |

The app makes the tables when it starts. `database_setup.sql` makes the
same tables by hand on MySQL. Dry, normal and wet are worked out from
the saved levels each time, so changing a level updates old readings too.

The readings are still simulated and are saved with `simulated` set to
true. An empty database is given one week of them so the charts have
something to show. The light shown on the dashboard is not a real light yet.

The look follows MyControl: the same palette, Space Grotesk font, line
icon style and bottom navigation on phones. The folders follow MyControl too.

## Progress

Done:
- FastAPI app and web pages: dashboard, history, settings, sign in and create account
- Database for readings, settings and accounts
- Sign in, sign out and accounts with hashed passwords
- Simulated readings, labelled as simulated
- Dry, normal and wet status
- Tests for the database and sign in
- Hardware list, wiring plan and architecture diagram

Not done yet:
- Fritzing diagram
- Testing the sensor and light on the Pi
- MQTT broker
- AWS deployment

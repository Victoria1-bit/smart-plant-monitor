# Smart Plant Monitoring and Automatic Watering System

An IoT system that measures soil moisture with a **Raspberry Pi 5**, shows
the plant's condition on a web dashboard and, in later stages, waters the
plant automatically with a small pump.

**Repository:** _link added after the GitHub repository is created_

> **Week 5 checkpoint status:** the FastAPI app and dashboard run on a laptop
> using **simulated** soil moisture readings. The physical sensor, pump, MQTT
> broker, database and AWS deployment have **not** been built or tested yet.
> Their code files are starter modules only.

---

## 1. Project concept

House plants often die because they are watered too much or too little.
This project puts a capacitive soil moisture sensor in the pot and connects
it to a Raspberry Pi 5. The Pi sends readings over **MQTT** to a **FastAPI**
web application, which stores them in a **database** and shows whether the
soil is **dry**, **normal** or **wet**. When the soil is dry, a small water
pump can be switched on, either automatically or by a logged-in user.
The finished system will be hosted on **AWS** behind a custom **HTTPS** domain.

## 2. Objectives

1. Read soil moisture from a capacitive sensor through an MCP3008 ADC on a Raspberry Pi 5.
2. Classify the soil as dry, normal or wet using configurable thresholds.
3. Send readings from the Pi to the server using MQTT publish/subscribe.
4. Store reading history in a database.
5. Display the live status and history on a FastAPI + Jinja2 dashboard.
6. Control a water pump safely (time limit, authentication required).
7. Deploy the application on AWS with a custom domain over HTTPS.

## 3. Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi 5 | Main controller |
| Capacitive soil moisture sensor | Measures soil moisture |
| MCP3008 ADC | Converts the sensor's analog voltage to a number (the Pi 5 has no analog inputs) |
| 3–5V mini water pump | Waters the plant |
| Logic-level MOSFET module + flyback diode | Lets a 3.3V GPIO pin safely switch the 5V pump |
| Separate 5V pump supply, breadboard, jumper wires, tubing | Supporting parts |

Full list: [docs/hardware-components.md](docs/hardware-components.md)
Wiring plan (for drawing the Fritzing diagram): [docs/wiring-plan.md](docs/wiring-plan.md)
System architecture diagram: [docs/architecture.md](docs/architecture.md)

## 4. Software

| Part | Technology |
|---|---|
| Web app and API | FastAPI (Python) |
| Dashboard | Jinja2 templates, HTML, CSS |
| Messaging | MQTT (Mosquitto broker, `paho-mqtt` client) |
| Hardware access on the Pi | `gpiozero` (RPi.GPIO does not support the Pi 5) |
| Database | Planned |
| Hosting | AWS EC2 with a custom HTTPS domain (planned) |

## 5. Project structure

```
iot-plant-monitor/
├── main.py              # FastAPI app: dashboard page and API routes
├── config.py            # Thresholds, calibration and settings (secrets come from .env)
├── plant.py             # Converts raw readings to %, decides dry / normal / wet
├── simulator.py         # SIMULATED sensor readings (used until hardware is ready)
├── schemas.py           # Pydantic models for API responses
├── mqtt_client.py       # STARTER: MQTT publish/subscribe (not tested)
├── hardware/
│   ├── sensor.py        # STARTER: read the real sensor via MCP3008 (not tested)
│   └── pump.py          # STARTER: run the pump with a safety time limit (not tested)
├── templates/
│   ├── layout.html      # Shared page layout
│   └── home.html        # Dashboard
├── static/css/main.css  # Dashboard styles
├── docs/                # Architecture, hardware list, wiring plan
├── requirements.txt     # Packages for the laptop/server
├── requirements-pi.txt  # Extra packages for the Raspberry Pi
└── .env.example         # Example settings (copy to .env, never commit .env)
```

## 6. How to run it (laptop)

First time only:

```bash
cd ~/iot-plant-monitor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Every time:

```bash
cd ~/iot-plant-monitor
source .venv/bin/activate
fastapi dev main.py
```

Then open:

- Dashboard: http://127.0.0.1:8000 (refreshes every 10 seconds)
- API docs: http://127.0.0.1:8000/docs

Press **Ctrl+C** to stop the server.

## 7. API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | HTML dashboard |
| GET | `/api/readings/latest` | Takes a new reading and returns it as JSON |
| GET | `/api/readings` | Last 20 readings, newest first |
| GET | `/api/health` | Returns `{"status": "ok"}` |

Every reading includes `"simulated": true` while the real sensor is not connected.

There is deliberately **no pump endpoint** yet: controlling a device over
the internet must require a login, which will be added first.

## 8. Plant status rules

| Moisture | Status |
|---|---|
| below 30% | Dry |
| 30% – 70% | Normal |
| above 70% | Wet |

These values are in `config.py`. The sensor calibration values
(`SENSOR_RAW_DRY`, `SENSOR_RAW_WET`) are typical defaults and must be
measured again with the real sensor.

## 9. Progress

| Item | Status |
|---|---|
| FastAPI starter app | ✅ Done, runs locally |
| Jinja2 dashboard | ✅ Done |
| Simulated readings, clearly labelled | ✅ Done |
| Dry / normal / wet status | ✅ Done |
| Hardware list, architecture, wiring plan | ✅ Done (documents) |
| Fritzing diagram | ⏳ To do, draw from `docs/wiring-plan.md` |
| Real sensor reading (`hardware/sensor.py`) | ⏳ Code written, not tested on hardware |
| Pump control (`hardware/pump.py`) | ⏳ Code written, not tested on hardware |
| MQTT (`mqtt_client.py`) | ⏳ Code written, no broker set up, not tested |
| Database | ⏳ To do |
| Login / authentication | ⏳ To do (needed before any pump endpoint) |
| AWS deployment with HTTPS domain | ⏳ To do |

## 10. References

- Corey Schafer, *Python FastAPI Tutorial* series (YouTube): app structure, Jinja2 templates, static files
- FastAPI documentation: https://fastapi.tiangolo.com
- gpiozero MCP3008 documentation: https://gpiozero.readthedocs.io/en/stable/api_spi.html
- Raspberry Pi GPIO pinout: https://pinout.xyz
- Eclipse Paho MQTT Python client: https://eclipse.dev/paho/
- Module resources on DkIT Moodle (Notes and Resources section)

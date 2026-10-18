"""
Project settings in one place.

Values are read from environment variables so that no passwords or
keys are ever written into the code. Copy .env.example to .env and
change the values there (.env is ignored by Git).
"""

import os

# --- Soil moisture thresholds (percent) ---
# Below DRY_THRESHOLD the plant needs water.
# Above WET_THRESHOLD the soil is too wet.
DRY_THRESHOLD = 30
WET_THRESHOLD = 70

# --- Sensor calibration (raw MCP3008 values, 0 to 1023) ---
# A capacitive sensor gives a HIGHER value when the soil is DRY.
# These are typical starting values. They must be re-measured with
# our own sensor (in air = dry, in a glass of water = wet).
SENSOR_RAW_DRY = 800
SENSOR_RAW_WET = 350

# --- Simulation ---
# True until the real sensor has been wired up and tested.
USE_SIMULATED_SENSOR = os.getenv("USE_SIMULATED_SENSOR", "true").lower() == "true"

# --- MQTT broker (not used yet, see mqtt_client.py) ---
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_MOISTURE = "plant/1/moisture"
MQTT_TOPIC_PUMP = "plant/1/pump"

# --- Pump (not used yet, see hardware/pump.py) ---
PUMP_GPIO_PIN = 17           # GPIO17 = physical pin 11
PUMP_MAX_SECONDS = 5         # safety limit so the pump can never run forever

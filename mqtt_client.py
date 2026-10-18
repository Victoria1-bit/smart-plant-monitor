"""
STARTER MODULE - MQTT publish/subscribe (NOT TESTED YET).

Plan:
    - The Raspberry Pi PUBLISHES moisture readings to  plant/1/moisture
    - The FastAPI app SUBSCRIBES to  plant/1/moisture  and saves them
    - The FastAPI app PUBLISHES pump commands to  plant/1/pump  (later, with login)

No broker has been set up yet. For local testing you can install
Mosquitto (brew install mosquitto) and run it with:  mosquitto -v

The broker address and login come from environment variables (see config.py),
so no passwords are stored in the code.
"""

import json

import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_TOPIC_MOISTURE,
)


def create_client(client_id):
    """Create an MQTT client and connect it to the broker."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    return client


def publish_reading(client, reading):
    """Send one reading (a dictionary) to the moisture topic as JSON."""
    message = json.dumps(reading)
    client.publish(MQTT_TOPIC_MOISTURE, message)


def on_message(client, userdata, msg):
    """Called every time a message arrives on a subscribed topic."""
    reading = json.loads(msg.payload)
    print(f"Received on {msg.topic}: {reading}")
    # TODO: save the reading to the database


def listen_for_readings():
    """Subscribe to the moisture topic and print every message (runs forever)."""
    client = create_client("plant-monitor-server")
    client.on_message = on_message
    client.subscribe(MQTT_TOPIC_MOISTURE)
    print(f"Listening on {MQTT_TOPIC_MOISTURE} ... (Ctrl+C to stop)")
    client.loop_forever()


if __name__ == "__main__":
    listen_for_readings()

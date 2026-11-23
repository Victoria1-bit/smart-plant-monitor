# MQTT publish and subscribe. NOT TESTED YET (no broker set up).
#
# The Pi will publish readings to "plant/moisture" and the FastAPI
# app will subscribe to them.

import json
import os

import paho.mqtt.client as mqtt

# Read from environment variables so no password is saved in the code
BROKER = os.getenv("MQTT_BROKER", "localhost")
USERNAME = os.getenv("MQTT_USERNAME", "")
PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC = "plant/moisture"


def connect():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, 1883)
    return client


def publish_reading(client, moisture):
    # Send one reading as JSON
    client.publish(TOPIC, json.dumps({"moisture": moisture}))


def on_message(client, userdata, msg):
    # Runs every time a reading arrives
    print(msg.topic, msg.payload.decode())


def listen():
    client = connect()
    client.on_message = on_message
    client.subscribe(TOPIC)
    client.loop_forever()

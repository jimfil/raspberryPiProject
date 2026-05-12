
import paho.mqtt.client as mqtt

import json
import time
import uuid
import os
import click
import threading
from queue import Queue, Full, Empty
from datetime import datetime, timezone
from typing import Dict, Any

from pirlib.sampler import PirSampler
from pirlib.interpreter import PirInterpreter
from apiFunc import find_sensor, find_bin


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def parse_iso_utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

# Default values
DEFAULT_SENSOR_ID = "urn:dev:team05:pir-01"
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883


def on_connect(client, userdata, flags, rc, topics):
    # rc == 0 means successful connection
    if rc == 0:
        print("Successfully connected to the broker!")
        for topic in topics:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Connection failed. Code: {rc}")

def on_message(client, userdata, msg, metrics, topic, out_file, verbose):
    # Callback that executes when a message is received from a topic.
    # - msg.topic: the topic from which the message came
    # - msg.payload: the content of the message (bytes)
    payload = msg.payload.decode('utf-8')
    print(f"Message received on: {msg.topic}")
    
    # Check if this is a status message
    if msg.topic.endswith("/status"):
        print(f"[Status] Producer status: {payload}")
        metrics["status_updates"] += 1
        return
    
    # Handle event messages
    try:
        with open(out_file, "a") as f:
            record = json.loads(payload)
            if verbose:
                print(f"Received message on topic '{msg.topic}': {record}")

            current_utc_iso = utc_now_iso()
            record["ingest_time"] = current_utc_iso
            event_dt  = parse_iso_utc(record["event_time"])
            ingest_dt = parse_iso_utc(current_utc_iso)

            latency_s = (ingest_dt - event_dt).total_seconds()
            record["pipeline_latency_ms"] = round(latency_s * 1000, 3)

            f.write(json.dumps(record) + "\n")
            f.flush()
            metrics["consumed"] += 1
            print(f"Latency: {record['pipeline_latency_ms']} ms")
    except Exception as e:
        print(f"Error processing the message: {e}")
        metrics["dropped"] += 1
    print(f"Statistics: {metrics['consumed']} messages consumed, {metrics['dropped']} messages dropped, {metrics['status_updates']} status updates.")

@click.command()
@click.option("--sensor-id", default=DEFAULT_SENSOR_ID, help="URN of the sensor to monitor")
@click.option("--broker", default="localhost", help="MQTT Broker address")
@click.option("--port", type=int, default=1883, help="MQTT Broker port")
@click.option("--qos", type=int, default=1, help="MQTT QoS (0=At most once, 1=At least once, 2=Exactly once)")
@click.option("--verbose", is_flag=True, help="Print status messages to the terminal")
def main(sensor_id: str, broker: str, port: int, qos: int, verbose: bool):
    # Load dynamic configuration
    sensor_data = find_sensor(sensor_id)
    if not sensor_data:
        print(f"Error: Sensor {sensor_id} not found in models.")
        return
    
    bin_urn = sensor_data.get("mounted_on")
    sensor_short_id = sensor_id.split(":")[-1]
    bin_short_id = bin_urn.split(":")[-1] if bin_urn else "unknown-bin"
    
    events_topic = f"smartbin/{bin_short_id}/{sensor_short_id}/events"
    status_topic = f"smartbin/{bin_short_id}/status"
    
    out_file = f"data/{sensor_short_id}_events.log"
    os.makedirs("data", exist_ok=True)

    # Creating an MQTT client
    client = mqtt.Client()
    # Connecting the callback functions so the client knows
    # what to do when connecting or receiving a message.
    metrics = {
        "consumed": 0,
        "dropped": 0,
        "status_updates": 0,
    }
    client.on_connect = lambda client, userdata, flags, rc: on_connect(client, userdata, flags, rc, [events_topic, status_topic])
    client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, metrics, events_topic, out_file, verbose)

    # Connecting to the MQTT broker.
    # keepalive=60 means the client will notify the broker that it is active every 60 seconds.
    client.connect(broker, port, keepalive=60)
    print("Waiting for messages... Press Ctrl+C to exit.")
    # loop_forever keeps the client running,
    # constantly listening for events (e.g., incoming messages).
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[consumer] shutting down...")
        client.disconnect()





if __name__ == "__main__":
    main()


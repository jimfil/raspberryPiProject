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


def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def parse_iso_utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
STATUS_TOPIC = "smartbin/bin-01/pir-01/status"


def on_connect(client, userdata, flags, rc, topic):
    # Callback that executes when the client connects to the broker.
    # rc == 0 means successful connection
    if rc == 0:
        print("Successfully connected to the broker!")
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
        client.subscribe(STATUS_TOPIC)
        print(f"Subscribed to topic: {STATUS_TOPIC}")
    else:
        print(f"Connection failed. Code: {rc}")

def on_message(client, userdata, msg, metrics, topic, out_file, verbose):
    # Callback that executes when a message is received from a topic.
    # - msg.topic: the topic from which the message came
    # - msg.payload: the content of the message (bytes)
    payload = msg.payload.decode('utf-8')
    print(msg.topic)
    # Check if this is a status message (retained)
    if msg.topic == STATUS_TOPIC:
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
@click.option("--broker", default="localhost", help="MQTT Broker address")
@click.option("--port", type=int, default=1883, help="MQTT Broker port")
@click.option("--topic", type=str, default="smartbin/bin-01/pir-01/events", help="MQTT topic for events")
@click.option("--qos", type=int, default=1, help="MQTT QoS (0=At most once, 1=At least once, 2=Exactly once)")
@click.option("--out", required=True, help="Path to the output JSONL file")
@click.option("--verbose", is_flag=True, help="Print status messages to the terminal")
def main(broker: str, port: int, topic: str, qos: int, out: str, verbose: bool):
    # Creating an MQTT client
    client = mqtt.Client()
    # Connecting the callback functions so the client knows
    # what to do when connecting or receiving a message.
    metrics = {
        "consumed": 0,
        "dropped": 0,
        "status_updates": 0,
    }
    client.on_connect = lambda client, userdata, flags, rc: on_connect(client, userdata, flags, rc, topic)
    client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, metrics, topic, out+".log", verbose)

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


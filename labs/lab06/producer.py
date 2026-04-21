import json
import time
import uuid
import os
import signal
from datetime import datetime, timezone

import click
import paho.mqtt.client as mqtt

from pirlib.sampler import PirSampler
from pirlib.interpreter import PirInterpreter

SENSOR_ID      = "urn:dev:team05:pir-01"
WASTEBIN_ID    = "urn:wastebin:bin-01"
ENVIRONMENT_ID = "urn:env:kypes-02"

_MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

def _load_context() -> dict:
    path = os.path.join(_MODELS_DIR, "context.jsonld")
    with open(path) as f:
        ctx = json.load(f)
    return ctx["@context"]

JSONLD_CONTEXT = _load_context()

def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

stop_flag = False

def handle_sigint(sig, frame):
    global stop_flag
    print("\n[Producer] Ανιχνεύθηκε Ctrl+C, τερματισμός...")
    stop_flag = True

@click.command()
@click.option("--device-id", default=SENSOR_ID, help="Unique identifier for this device")
@click.option("--pin", type=int, default=4, help="GPIO pin the PIR is connected to")
@click.option("--sample-interval", type=float, default=0.1, help="Seconds between sensor samples")
@click.option("--cooldown", type=float, default=2.0, help="Cooldown in seconds between motion events")
@click.option("--min-high", type=float, default=0.5, help="Minimum high time in seconds to trigger an event")
@click.option("--broker", default="localhost", help="MQTT Broker address")
@click.option("--port", type=int, default=1883, help="MQTT Broker port")
@click.option("--topic", default="smartbin/bin-01/pir-01/events", help="MQTT topic for events")
@click.option("--status-topic", default="smartbin/bin-01/pir-01/status", help="MQTT topic for sensor status")
@click.option("--qos", type=click.IntRange(0, 2), default=1, help="MQTT QoS (0=At most once, 1=At least once, 2=Exactly once)")
@click.option("--verbose", is_flag=True, help="Print status messages to the terminal")
def main(
    device_id: str,
    pin: int,
    sample_interval: float,
    cooldown: float,
    min_high: float,
    broker: str,
    port: int,
    topic: str,
    status_topic: str,
    qos: int,
    verbose: bool,
):
    global stop_flag
    signal.signal(signal.SIGINT, handle_sigint)

    # 1. Create an MQTT client
    client = mqtt.Client()
    
    # Setup Last Will and Testament (retained message on unexpected disconnect)
    client.will_set(status_topic, "offline", qos=1, retain=True)
    
    # 2. Connect to the broker
    if verbose:
        print(f"[Producer] Σύνδεση στον broker {broker}:{port}...")
    client.connect(broker, port, keepalive=60)
    
    # 3. Start the MQTT network loop
    client.loop_start()

    # Δημοσίευση ότι ο αισθητήρας είναι online (retained)
    client.publish(status_topic, "online", qos=1, retain=True)

    # 4. Set up the sampler and interpreter as before
    sampler = PirSampler(pin=pin)
    interp = PirInterpreter(cooldown_s=cooldown, min_high_s=min_high)

    # 5. Set run_id, seq counter
    run_id = str(uuid.uuid4())
    seq = 0

    print("[Producer] Ξεκίνησε η ανάγνωση του αισθητήρα (while not stopped). Πατήστε Ctrl+C για διακοπή.")
    
    # 6. While not stopped:
    while not stop_flag:
        current_time_s = time.time()
        
        # Read a sample from the sampler
        raw = sampler.read()
        
        # Update the interpreter
        events = interp.update(raw, current_time_s)

        # For each event the interpreter returns:
        for event in events:
            # Increment seq
            seq += 1
            
            # Build the event record (same fields as before, with JSON-LD context)
            record = {
                "@context":        JSONLD_CONTEXT,
                "@type":           "sosa:Observation",

                "device_id":       device_id,
                "sensor_ref":      device_id,
                "wastebin_ref":    WASTEBIN_ID,
                "environment_ref": ENVIRONMENT_ID,

                "event_time":      utc_now_iso(),
                "event_type":      "motion",
                "motion_state":    "detected",

                "seq":             seq,
                "run_id":          run_id,
            }
            
            # Convert the record to a JSON string
            payload = json.dumps(record)
            
            # Publish the JSON string to your chosen MQTT topic
            client.publish(topic, payload, qos=qos)
            
            # Print a status line if verbose
            if verbose:
                print(f"[Producer] Στάλθηκε event: {payload}")

        # Sleep for the sample interval
        time.sleep(sample_interval)

    # 7. On shutdown:
    if verbose:
        print("[Producer] Τερματισμός...")
    
    # Publish a retained status message ("offline") to a status topic
    client.publish(status_topic, "offline", qos=1, retain=True)
    time.sleep(0.5) # Μικρή παύση για να προλάβει να σταλεί το μήνυμα
    
    # Disconnect from the broker
    client.loop_stop()
    client.disconnect()
    
    if verbose:
        print("[Producer] Αποσύνδεση επιτυχής.")

if __name__ == "__main__":
    main()
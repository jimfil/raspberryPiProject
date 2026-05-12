import paho.mqtt.client as mqtt
import json
import time
import click
from datetime import datetime, timezone
from queue import Queue, Empty
from threading import Thread, Lock

event_times = Queue()
event_lock = Lock()


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode('utf-8').strip())
        if "motion_state" in data and data["motion_state"] == "detected":
            event_lock.acquire()
            event_times.put(time.time())
            event_lock.release()
    except Exception:
        pass  


def evaluate_usage(windowMinutes=10):
    cutoffTime = time.time() - (windowMinutes * 60)
    event_lock.acquire()
    while not event_times.empty() and event_times.queue[0] < cutoffTime:
        event_times.get()
    count = event_times.qsize() 
    event_lock.release()

    
    if count == 0:
        state = 'idle'
    elif count <=5:
        state = 'low'
    elif count <=15:
        state = 'medium'
    else:
        state = 'high'
        
    return (state,count)

@click.command()
@click.option("--broker", default="localhost", help="MQTT Broker address")
@click.option("--port", type=int, default=1883, help="MQTT Broker port")
@click.option("--subscribe-topic", default="smartbin/bin-01/pir-01/events", help="MQTT topic to subscribe to")
@click.option("--publish-topic", default="smartbin/bin-01/usage", help="MQTT topic to publish to")
@click.option("--window", type=int, default=10, help="Usage evaluation window in minutes")
@click.option("--interval", type=int, default=30, help="Time between evaluations in seconds")


def main(broker: str, port: int, subscribe_topic: str, publish_topic: str, window: int, interval: int):
    client = mqtt.Client(client_id="virtual-sensor-rules")
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(subscribe_topic)
    client.loop_start()
    print(f"[Virtual Sensor Rules] Monitoring {subscribe_topic} for usage evaluation window of {window} minutes")
    while True:
        state, count = evaluate_usage(window)
        payload = {
            "state": state,
            "count": count,
            "window_minutes": window,
            "timestamp": time.time()
        }
        client.publish(publish_topic, json.dumps(payload), qos=1, retain=True)
        print(f"[Virtual Sensor Rules] State: {state}, Count: {count}")
        time.sleep(interval)
    try:
        while True:
            state, count = evaluate_usage(window)
            payload = {
                "usage_level": state,
                "event_count": count,
                "window_size_minutes": window,
                "timestamp": time.time()
            }
            
            client.publish(publish_topic, json.dumps(payload), qos=1, retain=True)

            print(f"[Virtual Sensor Rules] State: {state}, Count: {count}")
            time.sleep(interval)
    except KeyboardInterrupt:
        client.disconnect()
        print("[Virtual Sensor Rules] Disconnected from broker.")

if __name__ == "__main__":
    main()
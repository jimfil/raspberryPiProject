import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.log")

def load_json(filepath):
    """Loads and parses a standard JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_events(filepath=EVENTS_FILE, limit=None, sensor_id=None):
    """Loads, filters, and sorts events from a JSONL file."""
    events = []

    if not os.path.exists(filepath):
        return events

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)

                record_sensor = record.get("device_id")

                if sensor_id is not None and record_sensor != sensor_id:
                    continue

                events.append(record)

            except json.JSONDecodeError:
                continue

    events.reverse()

    if limit is not None:
        events = events[:limit]

    return events

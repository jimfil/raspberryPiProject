import click
import json
import uuid
from datetime import datetime, timezone
import sys
import time
import os
from pirlib.sampler import PirSampler
from pirlib.interpreter import PirInterpreter

def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

@click.command()
@click.option('--device-id', required=True, type=str, help='identifies the mock wastebin device producing events')
@click.option('--pin', required=True, type=int, help='GPIO pin for PIR sensor')
@click.option('--sample-interval', type=float, default=0.1, help='Sample interval in seconds')
@click.option('--cooldown', type=float, default=0.0, help='Cooldown time in seconds')
@click.option('--min-high', type=float, default=0.0, help='Minimum high time in seconds')
@click.option('--duration', type=float, default=30.0, help='Duration to run in seconds')
@click.option('--out', required=True, type=click.Path(), help='output file path (append mode)')
@click.option('--verbose', is_flag=True, help='enable periodic operational output')

def generate_events(device_id, pin, sample_interval, cooldown, min_high, duration, out, verbose):
    if sample_interval < 0:
        print("Error: --sample-interval must be >= 0", file=sys.stderr)
        raise SystemExit(2)
    
    run_id = str(uuid.uuid4())
    deposit_total = 0
    written = 0

    sampler = PirSampler(pin)
    interp = PirInterpreter(cooldown_s=cooldown, min_high_s=min_high)

    t0 = time.time()
    end = t0 + duration

    try:
        with open(out, 'a', encoding='utf-8') as f:
            while time.time() < end:
                now = time.time()
                raw = sampler.read()
                for ev in interp.update(raw, now):
                    timestamp = utc_now_iso()
                    
                    if ev['kind'] == 'motion_detected':
                        deposit_total += 1
                        event_type = 'deposit'
                        record = {
                            "event_time": timestamp,
                            "ingest_time": timestamp,
                            "device_id": device_id,
                            "event_type": event_type,
                            "seq": written + 1,
                            "run_id": run_id,
                            "deposit_delta": 1,
                            "deposit_total": deposit_total
                        }
                    else:
                        event_type = 'pir_' + ev['kind']
                        record = {
                            "event_time": timestamp,
                            "ingest_time": timestamp,
                            "device_id": device_id,
                            "event_type": event_type,
                            "seq": written + 1,
                            "run_id": run_id
                        }

                    try:
                        f.write(json.dumps(record) + "\n")
                        f.flush()
                    except Exception as e:
                        print(f"Error writing to file: {e}", file=sys.stderr)
                        raise SystemExit(1)
                    
                    written += 1
                    print(f"t={ev['t']-t0:7.2f}s {ev['kind']} -> {event_type}")

                time.sleep(sample_interval)
                    
    except KeyboardInterrupt:
        print(f"\nInterrupted by user. Wrote {written} records.")
        raise SystemExit(0)

if __name__ == '__main__':
    generate_events()
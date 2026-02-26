import click
import json
import uuid
from datetime import datetime, timezone
import sys
import time
import os

def utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )

@click.command()
@click.option('--device-id', required=True, type=str, help='identifies the mock wastebin device producing events')
@click.option('--event-type', required=True, type=click.Choice(['deposit', 'heartbeat','lid_open','lid_close','maintenance_start','maintenance_end','sensor_error','waste_full']), help='deposit, heartbeat, lid_open, lid_close, maintenance_start, maintenance_end, sensor_error, waste_full')
@click.option('--count', required=True, type=int, help='number of records to emit')
@click.option('--interval', required=True, type=float, help='seconds between emissions')
@click.option('--out', required=True, type=click.Path(), help='output file path (append mode)')
@click.option('--starting-total', type=int, default=0, help='initial total count used for deposits')
@click.option('--verbose', is_flag=True, help='enable periodic operational output')


def generate_events(device_id, event_type, count, interval, out, starting_total, verbose):
    if count <= 0:
        print("Error: --count must be > 0", file=sys.stderr)
        raise SystemExit(2)
    if interval < 0:
        print("Error: --interval must be >= 0", file=sys.stderr)
        raise SystemExit(2)
    
    run_id = str(uuid.uuid4())
    deposit_total = starting_total
    written = 0

    try:
        with open(out, 'a', encoding='utf-8') as f:
            for seq in range(1, count + 1):
                timestamp = utc_now_iso()
                record = {
                    "event_time": timestamp,
                    "ingest_time": timestamp,
                    "device_id": device_id,
                    "event_type": event_type,
                    "seq": seq,
                    "run_id": run_id
                }

                if event_type == 'deposit':
                    deposit_total += 1
                    record["deposit_delta"] = 1
                    record["deposit_total"] = deposit_total
                elif event_type == 'lid_open':
                    record["lid_open"] = True
                elif event_type == 'lid_close':
                    record["lid_close"] = True
                elif event_type == 'maintenance_start':
                    record["maintenance_start"] = True
                elif event_type == 'maintenance_end':
                    record["maintenance_end"] = True
                elif event_type == 'sensor_error':
                    record["sensor_error"] = True
                elif event_type == 'waste_full':
                    record["waste_full"] = True
                elif event_type == 'heartbeat':
                    record["status"] = "online"


                try:
                    f.write(json.dumps(record) + "\n")
                    f.flush()
                except Exception as e:
                    print(f"Error writing to file: {e}", file=sys.stderr)
                    raise SystemExit(1)
                
                written += 1

                if verbose and seq % 5 == 0:
                    print(f"generated seq={seq} type={event_type} out={out}")

                if interval > 0 and seq < count:
                    time.sleep(interval)
                    
    except KeyboardInterrupt:
        print(f"\nInterrupted by user. Wrote {written} records.")
        raise SystemExit(0)

if __name__ == '__main__':
    generate_events()
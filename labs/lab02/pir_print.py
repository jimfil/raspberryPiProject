import time
import click
from pirlib.sampler import PirSampler
from pirlib.interpreter import PirInterpreter

@click.command()
@click.option("--pin", type=int, required=True, help="GPIO pin for PIR sensor")
@click.option("--sample-interval", type=float, default=0.1, help="Sample interval in seconds")
@click.option("--cooldown", type=float, default=0.0, help="Cooldown time in seconds")
@click.option("--min-high", type=float, default=0.0, help="Minimum high time in seconds")
@click.option("--duration", type=float, default=30.0, help="Duration to run in seconds")
def main(pin, sample_interval, cooldown, min_high, duration):
    sampler = PirSampler(pin)
    interp = PirInterpreter(cooldown_s=cooldown, min_high_s=min_high)

    t0 = time.time()
    end = t0 + duration

    print(f"[print] pin={pin} interval={sample_interval}s cooldown={cooldown}s min_high={min_high}s")

    try:
        while time.time() < end:
            now = time.time()
            raw = sampler.read()
            for ev in interp.update(raw, now):
                print(f"t={ev['t']-t0:7.2f}s {ev['kind']}")
            time.sleep(sample_interval)
    except KeyboardInterrupt:
        print("\n[print] Ctrl-C: exit.")

if __name__ == "__main__":
    main()

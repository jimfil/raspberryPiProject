# Lab 07 — Home Assistant Integration

## Section A: Runbook (How to run our code)

### Clone the Repository
If you haven't already cloned the repository, do so first:
```bash
git clone https://github.com/jimfil/raspberryPiProject.git
```

### Hardware Setup
Before running the code, ensure the PIR sensor is wired correctly to the Raspberry Pi:
- **VCC** -> Pin 2 (5V)
- **GND** -> Pin 6 (GND)
- **OUT** -> Pin 11 (GPIO17)

### Environment Setup / Activation (venv)
Navigate to the `labs/lab06` directory:
```bash
cd raspberryPiProject/labs/lab06
```

### Dependency Installation
Install the required packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Prerequisites: MQTT Broker
You need a running MQTT broker (e.g., Mosquitto) before starting the producer and consumer:

**On Raspberry Pi:**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

Verify the broker is running:
```bash
mosquitto_sub -h localhost -t "test/hello" &
mosquitto_pub -h localhost -t "test/hello" -m "Hello MQTT"
```

---

## Running with Docker Compose (Recommended on Raspberry Pi)

### Prerequisites
- Docker and Docker Compose installed on the Raspberry Pi or host system
- The host must have GPIO hardware available (for producer)

### Build and Start the Services
Docker Compose will automatically:
- Build the producer and consumer images from the Dockerfile
- Start the Mosquitto broker container with health checks
- Set up Docker networking so producer and consumer can reach the broker via hostname `broker`
- Mount volumes for persistence and output
- Set auto-restart policy

Run all services in detached mode:
```bash
docker compose up -d --build
```

### Check Logs
To see live output from all services:
```bash
docker compose logs -f
```

To see logs from a specific service:
```bash
docker compose logs -f producer
docker compose logs -f consumer
docker compose logs -f broker
```

### Stop All Services
To gracefully stop and remove all containers:
```bash
docker compose down
```

To stop and also remove volumes (careful: deletes data):
```bash
docker compose down -v
```

### Output Files
The JSONL output file is stored in a Docker volume (`output-data`). To access it:
```bash
docker cp mqtt-consumer:/data/motion_events.jsonl ./motion_events.jsonl
```

Or, find the volume location:
```bash
docker volume inspect output-data
```

### Docker Compose Architecture

The `docker-compose.yml` file defines three services:

1. **broker** (eclipse-mosquitto)
   - The MQTT message broker
   - Exposes port 1883 (MQTT) and 9001 (WebSocket)
   - Includes health checks to ensure readiness before producer/consumer start
   - Data persisted in `broker-data` and `broker-logs` volumes

2. **producer** (built from Dockerfile)
   - Reads PIR sensor on GPIO pin 17
   - Publishes motion events to `smartbin/bin-01/pir-01/events`
   - Publishes status to `smartbin/bin-01/pir-01/status`
   - Connects to broker using the service name `broker` (Docker DNS resolves this to the broker's IP)
   - Has GPIO hardware access (`/dev/gpiomem`, `/dev/gpiochip0`)


3. **consumer** (built from Dockerfile)
   - Subscribes to motion events from the producer
   - Writes JSONL records to `/data/motion_events.jsonl`
   - Output volume persisted in `output-data`
   - Connects to broker using the service name `broker`

**Key Points:**
- The `depends_on: broker: condition: service_healthy` ensures the broker is ready before producer/consumer start
- Service discovery: Producer and consumer use `--broker broker` instead of `--broker localhost`—Docker's internal DNS resolves `broker` to the broker container's IP
- Network isolation: All containers are on the same Docker network and can communicate via service names
- Volume management: Broker data, logs, and output are persisted in named volumes, surviving container restarts

---

## Manual Setup (Without Docker Compose)

### Exact Commands (copy/paste)

**Terminal 1 - Start the Producer** (on the Raspberry Pi with the PIR sensor):
```bash
python producer.py \
  --device-id "urn:dev:team05:pir-01" \
  --pin 17 \
  --sample-interval 0.1 \
  --cooldown 5.0 \
  --min-high 0.5 \
  --broker localhost \
  --port 1883 \
  --topic "smartbin/bin-01/pir-01/events" \
  --status-topic "smartbin/bin-01/pir-01/status" \
  --qos 1 \
  --verbose
```

**Terminal 2 - Start the Consumer** (can run on any machine with network access to broker):
```bash
python consumer.py \
  --broker localhost \
  --port 1883 \
  --topic "smartbin/bin-01/pir-01/events" \
  --qos 1 \
  --out motion_events.jsonl \
  --verbose
```
### Expected Outputs

For `producer.py` with `--verbose`, you should see:
```text
[Producer] Connecting to broker localhost:1883...
[Producer] Started reading the sensor (while not stopped). Press Ctrl+C to stop.
[Producer] Sent event: {'state': 'high', 'duration': 0.5}
[Producer] Sent event: {'state': 'low', 'duration': 5.2}
```

For `consumer.py` with `--verbose`, you should see:
```text
Successfully connected to the broker!
Subscribed to topic: smartbin/bin-01/pir-01/events
Subscribed to topic: smartbin/bin-01/pir-01/status
Received message on topic 'smartbin/bin-01/pir-01/events': {...}
Latency: 2.5 ms
Statistics: 5 messages consumed, 0 messages dropped, 1 status updates.
```

The output JSONL file (`motion_events.jsonl.log`) will contain records like:
```json
{"@context": {...}, "@type": "sosa:Observation", "device_id": "urn:dev:team05:pir-01", "sensor_ref": "urn:dev:team05:pir-01", "wastebin_ref": "urn:wastebin:bin-01", "environment_ref": "urn:env:kypes-02", "event_time": "2026-04-21T10:30:45.123Z", "event_type": "motion", "motion_state": "detected", "seq": 1, "run_id": "abc123-def456", "ingest_time": "2026-04-21T10:30:45.127Z", "pipeline_latency_ms": 4.0}
```

---

## Section B: Report



**RQ1: What is Home Assistant and what problem does it solve? Why use it instead of building a custom dashboard?**
Ans: 



RQ2: What is the difference between the “Home Assistant OS” and “Home Assistant Container” installation methods? Why did we use the Container method?
RQ3: What is an entity in Home Assistant? Give three examples of entities in your setup and their current states.


RQ4: How does Home Assistant learn about your sensors? Explain the MQTT discovery mechanism, what topic do you publish to, and what does the payload contain?
RQ5: Why should discovery messages be published with the retain flag (-r)?
RQ6: What is the device block in a discovery message? What happens in the Home Assistant UI when multiple entities share the same device.identifiers?
RQ7: What is the difference between a state_topic and a json_attributes_topic? When would you use each?


RQ8: List all the entities you created. For each one, give: the entity type (binary_sensor, sensor, counter, etc.), the state topic (if MQTT-based), and why you chose that type.
RQ9: What device_class did you use for your motion sensor? What does the device class affect in the Home Assistant UI?
RQ10: What additional entities did you create beyond the minimum? Why did you choose those?
RQ11: How did you group your entities under devices? Draw or describe the device → entity hierarchy.


RQ12: How does the Home Assistant Counter helper work? What services can you call on it?
RQ13: Paste the YAML of your “Count motion events” automation. Explain each part (trigger, condition, action).
RQ14: What other automation(s) did you create? Paste the YAML and explain the trigger, condition (if any), and action.
RQ15: Give one example of an automation that would be useful in a real Smart Wastebin deployment that involves a condition (not just trigger → action). Describe the trigger, the condition, and the action.


RQ16: Your producer now publishes to two kinds of topics: the data topic (full JSON events for the consumer) and the HA state topics (simple values for Home Assistant). Why not use the same topic for both?
RQ17: Show a screenshot of your Home Assistant dashboard with your wastebin entities visible.
RQ18: What happens in Home Assistant when the producer is stopped? Does the motion sensor show “unavailable”, “clear”, or something else? How could you improve this?


RQ19: Compare the effort of building a custom web dashboard vs. using Home Assistant. What do you gain? What do you give up?
RQ20: Home Assistant runs locally on the Pi, no cloud needed. Why does this matter for an edge IoT deployment?
RQ21: If your project had 10 wastebins with 3 sensors each, how would the MQTT discovery approach scale compared to manually configuring 30 entities?

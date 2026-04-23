# Lab 06 — MQTT Publish-Subscribe Architecture

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

Create a virtual environment:
```bash
python3 -m venv venv
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
- Apply resource limits (CPU and memory)
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
   - Runs with CPU and memory limits

3. **consumer** (built from Dockerfile)
   - Subscribes to motion events from the producer
   - Writes JSONL records to `/data/motion_events.jsonl`
   - Output volume persisted in `output-data`
   - Connects to broker using the service name `broker`
   - Runs with CPU and memory limits

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



**RQ1: What is the role of the MQTT broker? Why don’t we just let the producer and consumer communicate directly (e.g via sockets)?**

Ans: MQTT follows the publish-subscribe model, where clients communicate with a central server called a broker. The broker has some advantages over direct communication, which are: the producer and the consumer just connect to the broker without having direct connection which requires for both of them to be online and know eachothers IP address, the distribution of information through the broker to multiple consumers is easier than a producer connecting directly to them, the reconnection in MQTT brokers is handled automatically and data is queued during downtime and lastly the MQTT broker has simplified security mechanisms, independent from producer and consumer devices. 



**RQ2: What topic structure did you choose and why? How does it support future extensibility (more sensors, more bins)?**

Ans: We chose the hierarchical topic structure: `smartbin/<bin-id>/<sensor-id>/events` and `smartbin/<bin-id>/<sensor-id>/status`. This structure is chosen because it organizes data by domain (smartbin), then by physical device (bin), then by specific sensor, and finally by data type (events or status). This is highly extensible: to add a new bin, we just add a new `<bin-id>` segment; to add a new sensor type to an existing bin, we add a new `<sensor-id>`. Multiple consumers can subscribe using wildcards like `smartbin/+/+/events` to get all events from all bins and sensors, or `smartbin/bin-01/+/events` to get all sensor events from a specific bin.



**RQ3: Explain the difference between QoS 0, 1, and 2 in your own words. Which did you use for your motion events and why?**

Ans: QoS 0 (At Most Once) means the broker sends the message once and does not wait for acknowledgment—fast but messages can be lost. QoS 1 (At Least Once) means the broker sends the message and waits for acknowledgment; if not received, it resends—guarantees delivery but messages might be duplicated. QoS 2 (Exactly Once) means the broker uses a handshake protocol to ensure the message is delivered exactly once—slowest but most reliable. For motion events, we used QoS 1 because motion detection is time-sensitive and we need to guarantee each event is delivered, but occasional duplicates are acceptable and can be deduplicated by the consumer using the sequence number in the record.



**RQ4: What is a retained message? Give one concrete example of when it would be useful for your system.**

Ans: A retained message is a message which has a flag activated which enables the message to remain for future subscribers. A retained message would be useful for transferring basic data for our smart bin like status(online, offline; back in x hours,...).



**RQ5: When you subscribed to smartbin/+/motion, which messages did you receive and which did you not? Explain why, based on how + works.**

Ans: When subscribing to `smartbin/+/motion`, we received messages from topics like `smartbin/bin-01/motion`, `smartbin/bin-02/motion`, etc. We did NOT receive messages from `smartbin/bin-01/pir-01/motion` or `smartbin/bin-01/pir-01/events/motion` because the `+` wildcard matches exactly ONE topic level. Since our actual topic structure is `smartbin/<bin-id>/<sensor-id>/<data-type>`, the `+` only covers one of those segments, so it would match `smartbin/+/events` (all sensors, all bins, events only) but not messages with more or fewer levels in the topic hierarchy.



**RQ6: What happened when you subscribed to #? Why is this useful for debugging but dangerous in production?**

Ans: The wildcard subscription '#' allows us to observe: the entire data flow of a specified topic, the whole timeline of a bug occuring without having to look at disparate log files, which is critical for time-sensitive production issues. It also helps us in tracking and identifying messages sent to wrong topics, or messages with the wrong data format, so it acts as a 'monitor' of the entire topic. But it can be dangerous in production mainly because of the sheer amount of data being transferred through the broker, which could result in potentially slowing down or crashing the message broker, in the client's inability to process the information, leading to memory saturation and out-of-memory errors, or in receiving sensitive client information.  



**RQ7: You published a message while no subscriber was connected (without the retain flag). Then you started a subscriber. Did it receive the message? Why or why not?**

Ans: The subscriber did not receive the message because the broker had no subcribers, so the message without the retained flag was not retained by the broker.



**RQ8: What are the main differences between your run_pipeline.py (threaded queue) and the new producer.py + consumer.py (MQTT)?**

Ans: The threaded queue version (Lab 05) uses local in-process communication through a Python Queue, tightly coupling producer and consumer threads within a single process on the same machine. It uses a drop-newest policy for backpressure when the queue is full. The MQTT version (Lab 06) decouples producer and consumer completely—they run in separate processes/machines and communicate through a central broker. MQTT provides automatic message queuing on the broker side, automatic reconnection, retained messages, QoS guarantees, and pub/sub wildcard subscriptions. The MQTT version is also distributed (can run producer on Pi and consumer on laptop) whereas the threaded version is local-only. Finally, MQTT is language-agnostic and network-transparent; the threaded version is Python-specific.



**RQ9: In the threaded version, what happened when the queue was full? In the MQTT version, what happens if the consumer is slow or offline?**

Ans: In the threaded version, if the queue was full, the messages would be lost. But in the MQTT version, given that the consumer is subscribed, the messages would be retained by the broker.



**RQ10: How does the callback pattern in paho-mqtt (on_message) differ from the polling pattern you used in the threaded consumer (queue.get(timeout=0.5))?**

Ans: The polling pattern (queue.get with timeout) is synchronous—the consumer thread actively waits and blocks until a message arrives or the timeout expires. The callback pattern (on_message) is event-driven—the MQTT client library runs an event loop in the background and invokes the callback function whenever a message arrives, without the consumer code needing to poll. Callbacks are more efficient (no busy-waiting) but require careful handling of concurrent access and shared state. Polling is simpler to understand and debug (sequential flow) but less efficient if the arrival rate is low.



**RQ11: Show one example JSON record from the MQTT-based consumer. Is the structure the same as in previous labs? What about pipeline_latency_ms, is it higher or lower? Why?**

Ans: Example record:
```json
{
  "@context": {...},
  "@type": "sosa:Observation",
  "device_id": "urn:dev:team05:pir-01",
  "sensor_ref": "urn:dev:team05:pir-01",
  "wastebin_ref": "urn:wastebin:bin-01",
  "environment_ref": "urn:env:kypes-02",
  "event_time": "2026-04-21T10:30:45.123Z",
  "event_type": "motion",
  "motion_state": "detected",
  "seq": 1,
  "run_id": "d1f3a2b4-5678-9abc-def0-123456789abc",
  "ingest_time": "2026-04-21T10:30:45.127Z",
  "pipeline_latency_ms": 4.0
}
```
The structure is identical to previous labs (JSON-LD format with @context and @type). The pipeline_latency_ms is typically LOWER in the MQTT version (4-10 ms range) compared to the threaded queue version (10-50 ms range) because MQTT broker-to-client communication is optimized for low latency, and there's no local queue contention. However, if the consumer is on a remote machine, latency can be higher due to network RTT.



**RQ12: You stopped the consumer and kept the producer running. What happened to the messages published during that time? Were they delivered when the consumer restarted?**

Ans: When the consumer was offline, the producer continued publishing messages to the broker with QoS 1. The broker stored these messages in memory (since they were not retained messages; retained messages persist even after the broker restarts). When the consumer reconnected and resubscribed to the topic, the broker delivered all queued messages to the consumer. The consumer received them and added ingest_time/latency stamps, creating a "catch-up" period where it processed the backlog. This demonstrates MQTT's store-and-forward capability, which is crucial for reliable IoT systems where consumers may be temporarily offline.



**RQ13: You ran two consumers on the same topic. Did both receive every message? Why does this matter for building scalable systems?**

Ans: The consumers both received the same message. This is important for building scalable systems because, for example in our case, we need to inform the waste management agency and our system that our smart bin is full.



**RQ14: Could you run the producer on one Raspberry Pi and the consumer on a different machine (e.g., your laptop)? What would you need to change?**

Ans: We can do that. First, we need to update mosquitto.conf, so the broker can communicate with other devices in our local network. to do that, we open the config file: "sudo nano /etc/mosquitto/mosquitto.conf",  and we use the instructions: "listener 1883 0.0.0.0 \n allow_anonymous true" to allow the broker to listen to any ip address in our network, without needing a username or a password. Then, we restart the system: "sudo systemctl restart mosquitto". Then we need to find the IP of the Pi(producer) and our computer(consumer), and replace them to the corresponnding Python files for the consumer and the producer.



**RQ15: In your own words, what does “decoupling” mean in the context of pub/sub? What are the practical benefits?**

Ans: Decoupling means breaking down the dependency between the publisher and subscriber, and instead using a message broker or a topic as a middleman. We mentioned some of the benefits of the MQTT broker in earlier questions. A synopsy of the benefits of decoupling are: efficient communication to a high number of consumers, the subscriber being offline does not mean the message will get lost; the message will be retained, improved scalability and performance.



**RQ16: If the Mosquitto broker itself crashes, what happens to your system? How could you mitigate this?**

Ans: If the MQTT broker crashes, it is going to result in a total and immediate communication blackout between producers and consumers, automated devices like edge devices that rely on data from a sensor will stop and there is a risk of loss of data without the broker. We could mitigate the effects of a crash by rebooting or restarting the broker automatically, by saving the data and the messages being transferred to a disk, and by using QoS 1 (At least once) or QoS 2 (Exactly once) for crucial messages. This ensures that if the broker drops a message, the client will re-send it upon reconnection.



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

Run the producer:
```bash
python producer.py --broker localhost --port 1883 --device-id pir-01 --pin 17 --verbose
```

And open on a browser the home assistant dashboard on `http://{pi's ip address}:8123`.
---

## Section B: Report



**RQ1: What is Home Assistant and what problem does it solve? Why use it instead of building a custom dashboard?**

Ans: Home Assistant is an open-source platform designed for home automation. It acts like a local control center for your smart home through a web-based dashboard where you can monitor the state of devices and sensors. Home Assistant offers us a dashboard, a state manager, an automation engine, and a history database, basically an all in one, without us having to create all these things from scratch.



**RQ2: What is the difference between the “Home Assistant OS” and “Home Assistant Container” installation methods? Why did we use the Container method?**

Ans: The “Home Assistant OS” method integrates the Home Assistant in a device completely, like a normal OS, while the “Home Assistant Container” method isolates the Home Assistant in a container using the docker. We used the “Home Assistant Container” method so we can run Home Assistant in an isolated environment, without the Home Assistant OS interfering with or taking over our Pi operating system.



**RQ3: What is an entity in Home Assistant? Give three examples of entities in your setup and their current states.**

Ans: Entities are the basic building blocks to hold data in Home Assistant. An entity represents a sensor, action, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. In our setup:

1. **PIR Motion Sensor** (`binary_sensor.pir_motion_sensor`) — state: `clear` (no motion) or `detected` (motion present).
2. **Wastebin Status** (`sensor.wastebin_status`) — state: `active` or `offline`, with JSON attributes `location`, `last_motion`, and `total_events_today`.
3. **Motion Event Count** (`sensor.motion_event_count`) — state: a numeric value (e.g., `5`) representing the total number of motion events detected since the producer started, measured in `events`.



**RQ4: How does Home Assistant learn about your sensors? Explain the MQTT discovery mechanism, what topic do you publish to, and what does the payload contain?**

Ans: Home Assistant learns about sensors via MQTT Discovery by listening for JSON configuration messages published by devices to specific topics on an MQTT broker. This automated process allows devices to identify themselves, their capabilities, and their state topics, allowing Home Assistant to auto-configure them without manual YAML entry.

We published three discovery messages (all with `retain=True`):

- **Topic:** `homeassistant/binary_sensor/pir_01_motion/config`  
  **Payload:**
  ```json
  {
    "name": "PIR Motion Sensor",
    "state_topic": "smartbin/bin-01/pir-01/motion",
    "payload_on": "detected",
    "payload_off": "clear",
    "device_class": "motion",
    "unique_id": "pir_01_motion",
    "device": {"identifiers": ["pir-01"], "name": "PIR Sensor 01", "model": "HC-SR501", "manufacturer": "Generic"}
  }
  ```

- **Topic:** `homeassistant/sensor/wastebin_01_status/config`  
  **Payload:**
  ```json
  {
    "name": "Wastebin Status",
    "state_topic": "smartbin/bin-01/status",
    "value_template": "{{ value_json.state }}",
    "json_attributes_topic": "smartbin/bin-01/status",
    "unique_id": "wastebin_01_status",
    "device": {"identifiers": ["bin-01"], "name": "Smart Wastebin 01", "model": "Smart Wastebin v1", "manufacturer": "Jumbo xoreuo"}
  }
  ```

- **Topic:** `homeassistant/sensor/wastebin_01_motion_count/config`  
  **Payload:**
  ```json
  {
    "name": "Motion Event Count",
    "state_topic": "smartbin/bin-01/pir-01/event_count",
    "unit_of_measurement": "events",
    "icon": "mdi:motion-sensor",
    "unique_id": "wastebin_01_motion_count",
    "device": {"identifiers": ["bin-01"], "name": "Smart Wastebin 01"}
  }
  ```



**RQ5: Why should discovery messages be published with the retain flag (-r)?**

Ans: The retain flag allows the Home Assistant to detect the message even if it restarts after the message was published.



**RQ6: What is the device block in a discovery message? What happens in the Home Assistant UI when multiple entities share the same device.identifiers?**

Ans: The device block in an MQTT discovery message is a JSON object within the configuration payload that enables Home Assistant to group multiple entities (sensors, switches, etc.) under a single physical or logical device in the UI. When multiple MQTT discovery messages share the same device.identifiers, Home Assistant creates a single device entry in the UI and automatically lists all associated entities together, essentially grouping the entities with common functions.



**RQ7: What is the difference between a state_topic and a json_attributes_topic? When would you use each?**

Ans: 
state_topic: Defines the main topic for the entity's primary state (e.g., ON/OFF, temperature value).

json_attributes_topic: Subscribes to a JSON payload to populate additional information (attributes) about the entity (e.g., battery level, signal strength).



**RQ8: List all the entities you created. For each one, give: the entity type (binary_sensor, sensor, counter, etc.), the state topic (if MQTT-based), and why you chose that type.**

Ans:

| Entity Name | Type | State Topic | Reason |
|---|---|---|---|
| PIR Motion Sensor | `binary_sensor` | `smartbin/bin-01/pir-01/motion` | Motion is a binary state (detected / clear), so `binary_sensor` is the correct type. |
| Wastebin Status | `sensor` | `smartbin/bin-01/status` | The status carries multiple values (state, location, last_motion, event count) encoded as JSON, so a `sensor` with `value_template` and `json_attributes_topic` was ideal. |
| Motion Event Count | `sensor` | `smartbin/bin-01/pir-01/event_count` | A running numeric counter needs a `sensor` with a unit of measurement (`events`). A HA Counter helper was not used here because the producer maintains the count and publishes it directly. |
| Wastebin Motion Counter | `counter` | None | This is a HA helper entity (not MQTT-based) that is incremented by the "Motion Alert" automation. It provides a persistent daily count separate from the MQTT event stream, enabling more flexible automation logic and historical tracking within HA. |


We have the excluded the automations from this list as they are provided below in RQ13 and RQ14.


**RQ9: What device_class did you use for your motion sensor? What does the device class affect in the Home Assistant UI?**

Ans: We used `device_class: motion` for the PIR motion sensor. The device class affects the Home Assistant UI in several ways: it determines the icon displayed for the entity (a motion-wave icon instead of a generic sensor icon), sets the human-readable state labels (`Detected` / `Clear` instead of raw `ON`/`OFF`), controls how the entity appears in dashboards and history graphs, and enables HA to correctly categorise it in the "Binary Sensors" section of the device page.



**RQ10: What additional entities did you create beyond the minimum? Why did you choose those?**

Ans: Beyond the minimum required binary motion sensor, we added two extra entities:

1. **Wastebin Status** (`sensor`) — provides richer context about the bin (location, last motion timestamp, total events today, online/offline state). This is useful for operational monitoring without having to look at raw MQTT messages.
2. **Motion Event Count** (`sensor`) — tracks the cumulative number of motion events. This allows trend analysis (e.g., how busy a bin is over time) directly from the HA dashboard and history graphs.



**RQ11: How did you group your entities under devices? Draw or describe the device → entity hierarchy.**

Ans: We used the `device` block in each discovery payload with shared `identifiers` to group entities. The hierarchy is:

```
PIR Sensor 01  (identifier: "pir-01", model: HC-SR501)
└── PIR Motion Sensor  (binary_sensor)

Smart Wastebin 01  (identifier: "bin-01", model: Smart Wastebin v1)
├── Wastebin Status      (sensor)
└── Motion Event Count  (sensor)
```

The PIR sensor entity is registered under the **PIR Sensor 01** device because it represents the physical hardware sensor. The status and count entities are registered under **Smart Wastebin 01** because they describe the state of the bin as a whole, not just the PIR chip.



**RQ12: How does the Home Assistant Counter helper work? What services can you call on it?**

Ans: The Home Assistant Counter helper works by incrementing a counter every time an MQTT message is received on the configured topic. It allows you to define a maximum value and a reset value. You can call services on it to reset the counter or manually increment it.



**RQ13: Paste the YAML of your “Count motion events” automation. Explain each part (trigger, condition, action).**

Ans:
```yaml
alias: Count Motion Events
description: ""
triggers:
  - trigger: state
    entity_id:
      - binary_sensor.pir_sensor_01_pir_motion_sensor
    to:
      - "on"
    from:
      - "off"
conditions: []
actions:
  - action: counter.increment
    target:
      entity_id: counter.wastebin_motion_count
    data: {}
mode: single
```

- **Trigger:** Fires every time `binary_sensor.pir_sensor_01_pir_motion_sensor` transitions **from** `off` **to** `on` — meaning a new motion detection event just started. Using both `from` and `to` prevents the automation from firing on the `off → off` edge that can occur during HA restarts.
- **Condition:** None (`conditions: []`) — every rising edge unconditionally increments the counter, no extra checks needed.
- **Action:** Calls `counter.increment` on `counter.wastebin_motion_count`, adding 1 to the persistent counter entity.
- **Mode `single`:** If motion fires again before the action finishes (virtually instant here), duplicate runs are ignored, preventing double-counts.



**RQ14: What other automation(s) did you create? Paste the YAML and explain the trigger, condition (if any), and action.**

Ans:
```yaml
alias: Daily counter reset
description: ""
triggers:
  - trigger: time
    at: "00:00:00"
    weekday:
      - sun
      - mon
      - tue
      - wed
      - thu
      - fri
      - sat
conditions: []
actions:
  - action: counter.reset
    metadata: {}
    target:
      entity_id: counter.wastebin_motion_count
    data: {}
  - action: persistent_notification.create
    metadata: {}
    data:
      title: Daily counter reset
      message: Counter reset
mode: single
```

**Daily counter reset — explanation:**
- **Trigger:** A `time` trigger fires every day at exactly **midnight (00:00:00)**, every day of the week (`sun` through `sat`).
- **Condition:** None — the reset always happens at midnight regardless of any other state.
- **Actions (two steps):**
  1. `counter.reset` — resets `counter.wastebin_motion_count` back to 0, giving a clean daily count.
  2. `persistent_notification.create` — posts a brief "Counter reset" notification in the HA UI so operators know the daily cycle restarted.
- **Mode `single`:** Prevents any accidental duplicate reset if the clock fires more than once.

```yaml
alias: High activity alert
description: ""
triggers:
  - trigger: state
    entity_id:
      - counter.wastebin_motion_count
conditions:
  - condition: numeric_state
    entity_id: counter.wastebin_motion_count
    above: 50
    below: 998.8
actions:
  - action: persistent_notification.create
    metadata: {}
    data:
      title: High Usage Alert
      message: "Smart Wastebin Full "
mode: single

```

**High activity alert — explanation:**
- **Trigger:** Fires whenever the state of `counter.wastebin_motion_count` changes (i.e., every time the counter increments).
- **Condition:** `numeric_state` — the notification is only sent when the counter value is **above 50** and **below 998.8** (≈ the counter's max). This means alerts fire once the bin has seen more than 50 motion events in the current day, indicating high usage, but stops before the counter rolls over at its maximum.
- **Action:** `persistent_notification.create` posts a "Smart Wastebin Full" alert in the HA UI.
- **Mode `single`:** Ensures only one alert is active at a time while the counter keeps climbing.

```yaml
alias: Motion Alert
description: ""
triggers:
  - type: motion
    device_id: ed164895ea709143270a80a71561cd58
    entity_id: 5acbe301b5371dcd759f4fb7aff6f7c5
    domain: binary_sensor
    trigger: device
    for:
      hours: 0
      minutes: 0
      seconds: 2
conditions: []
actions:
  - action: persistent_notification.create
    metadata: {}
    data:
      message: Motion detected at Smart Wastebin 01 — {{ now().strftime('%H:%M:%S') }}
      title: Wastebin Alert
mode: single
```

**Motion Alert — explanation:**
- **Trigger:** A `device` trigger tied to the physical PIR binary sensor device (referenced by `device_id` and `entity_id` internal HA identifiers). It fires when the sensor reports a **motion** event that has been sustained for **2 seconds** (`for: seconds: 2`), filtering out brief spurious spikes.
- **Condition:** None — any confirmed 2-second motion event triggers the notification.
- **Action:** `persistent_notification.create` sends a timestamped alert: *"Motion detected at Smart Wastebin 01 — HH:MM:SS"*. The timestamp is rendered live using the Jinja2 template `{{ now().strftime('%H:%M:%S') }}`.
- **Mode `single`:** If another motion event arrives before the action completes, the duplicate is dropped.


**RQ15: Give one example of an automation that would be useful in a real Smart Wastebin deployment that involves a condition (not just trigger → action). Describe the trigger, the condition, and the action.**

Ans: An automation that would be useful in a smart wastebin system is the ability to detect when the bin is full. A useful automation to prevent overflow involves a trigger (ultrasonic sensor measuring high trash level), a condition (time of day is before 8:00 AM), and an action (send a notification to staff to empty it immediately).



**RQ16: Your producer now publishes to two kinds of topics: the data topic (full JSON events for the consumer) and the HA state topics (simple values for Home Assistant). Why not use the same topic for both?**

Ans:



**RQ17: Show a screenshot of your Home Assistant dashboard with your wastebin entities visible.**

Ans:



**RQ18: What happens in Home Assistant when the producer is stopped? Does the motion sensor show “unavailable”, “clear”, or something else? How could you improve this?**

Ans:



**RQ19: Compare the effort of building a custom web dashboard vs. using Home Assistant. What do you gain? What do you give up?**

Ans: Using home Assistant, you can have a functional dashboard in minutes due to automatic device discovery and default "Overview" dashboards. However, achieving a highly polished, specific aesthetic requires a steep learning curve involving YAML, custom "strategies," and community themes. In the other hand, building a dashboard from scratch (e.g., using React or Vue) requires you to manually write code for every interaction and display element. You must also handle the "backend" logic/authentication, state management, and connecting to thousands of potential device APIs that HA handles out of the box.



**RQ20: Home Assistant runs locally on the Pi, no cloud needed. Why does this matter for an edge IoT deployment?**

Ans: Home Assistant running locally on a Raspberry Pi—without needing the cloud—is a foundational approach to edge IoT deployment. It matters because it ensures that data processing, automation logic, and device control happen on-site rather than in a distant data center, providing critical advantages in reliability, privacy, speed, and long-term viability. 



**RQ21: If your project had 10 wastebins with 3 sensors each, how would the MQTT discovery approach scale compared to manually configuring 30 entities?**

Ans: MQTT discovery scales significantly better than manual configuration for a project with 10 wastebins (30 sensors/entities), transforming a tedious manual process into an automated, plug-and-play system. With MQTT Discovery, the device (sensor node) registers itself with Home Assistant upon powering up, whereas manual configuration requires creating 30 separate configuration entries in YAML, wastin a lot of time of setting and maintenance.



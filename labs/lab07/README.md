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

## Section B: Report



**RQ1: What is Home Assistant and what problem does it solve? Why use it instead of building a custom dashboard?**

Ans: Home Assistant is an open-source platform designed for home automation. It acts like a local control center for your smart home through a web-based dashboard where you can monitor the state of devices and sensors. Home Assistant offers us a dashboard, a state manager, an automation engine, and a history database, basically an all in one, without us having to create all these things from scratch.



**RQ2: What is the difference between the “Home Assistant OS” and “Home Assistant Container” installation methods? Why did we use the Container method?**

Ans: The “Home Assistant OS” method integrates the Home Assistant in a device completely, like a normal OS, while the “Home Assistant Container” method isolates the Home Assistant in a container using the docker. We used the “Home Assistant Container” method so we can run Home Assistant in an isolated environment, without the Home Assistant OS interfering with or taking over our Pi operating system.



**RQ3: What is an entity in Home Assistant? Give three examples of entities in your setup and their current states.**

Ans: Entities are the basic building blocks to hold data in Home Assistant. An entity represents a sensor, action, or function in Home Assistant. Entities are used to monitor physical properties or to control other entities. In our setup,



**RQ4: How does Home Assistant learn about your sensors? Explain the MQTT discovery mechanism, what topic do you publish to, and what does the payload contain?**

Ans: Home Assistant learns about sensors via MQTT Discovery by listening for JSON configuration messages published by devices to specific topics on an MQTT broker. This automated process allows devices (like ESP8266 or Node-RED) to identify themselves, their capabilities, and their state topics, allowing Home Assistant to auto-configure them without manual YAML entry. We published to the topic: "", a configuration message containig the payload:



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



**RQ9: What device_class did you use for your motion sensor? What does the device class affect in the Home Assistant UI?**

Ans:



**RQ10: What additional entities did you create beyond the minimum? Why did you choose those?**

Ans:



**RQ11: How did you group your entities under devices? Draw or describe the device → entity hierarchy.**

Ans:



**RQ12: How does the Home Assistant Counter helper work? What services can you call on it?**

Ans: The Home Assistant Counter helper works by incrementing a counter every time an MQTT message is received on the configured topic. It allows you to define a maximum value and a reset value. You can call services on it to reset the counter or manually increment it.



**RQ13: Paste the YAML of your “Count motion events” automation. Explain each part (trigger, condition, action).**

Ans:



**RQ14: What other automation(s) did you create? Paste the YAML and explain the trigger, condition (if any), and action.**

Ans:



**RQ15: Give one example of an automation that would be useful in a real Smart Wastebin deployment that involves a condition (not just trigger → action). Describe the trigger, the condition, and the action.**

Ans: An automation that would be useful in a smart wastebin system is the ability to detect when the bin is full. A useful automation to prevent overflow involves a trigger (ultrasonic sensor measuring high trash level), a condition (time of day is before 8:00 AM), and an action (send a notification to staff to empty it immediately).



**RQ16: Your producer now publishes to two kinds of topics: the data topic (full JSON events for the consumer) and the HA state topics (simple values for Home Assistant). Why not use the same topic for both?**

Ans:



**RQ17: Show a screenshot of your Home Assistant dashboard with your wastebin entities visible.**

Ans:



**RQ18: What happens in Home Assistant when the producer is stopped? Does the motion sensor show “unavailable”, “clear”, or something else? How could you improve this?**

Ans:



**RQ19: Compare the effort of building a custom web dashboard vs. using Home Assistant. What do you gain? What do you give up?**

Ans:



**RQ20: Home Assistant runs locally on the Pi, no cloud needed. Why does this matter for an edge IoT deployment?**

Ans: Home Assistant running locally on a Raspberry Pi—without needing the cloud—is a foundational approach to edge IoT deployment. It matters because it ensures that data processing, automation logic, and device control happen on-site rather than in a distant data center, providing critical advantages in reliability, privacy, speed, and long-term viability. 



**RQ21: If your project had 10 wastebins with 3 sensors each, how would the MQTT discovery approach scale compared to manually configuring 30 entities?**

Ans: MQTT discovery scales significantly better than manual configuration for a project with 10 wastebins (30 sensors/entities), transforming a tedious manual process into an automated, plug-and-play system. With MQTT Discovery, the device (sensor node) registers itself with Home Assistant upon powering up, whereas manual configuration requires creating 30 separate configuration entries in YAML, wastin a lot of time of setting and maintenance.



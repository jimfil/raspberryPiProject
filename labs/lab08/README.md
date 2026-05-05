# Lab 08 — Building a REST API for the Smart Wastebin

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
Navigate to the `labs/lab08` directory:
```bash
cd raspberryPiProject/labs/lab08
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



**RQ1: Write down your complete API design, every endpoint, its HTTP method, the URI, what parameters it accepts, and what it returns. Present this as a table.**

Ans:



**RQ2: Why do the event-listing endpoints use GET and not POST? RQ3: Why does the “mark as emptied” endpoint use POST and not PUT? Think about idempotency.**

Ans:



**RQ4: How did you handle the case where a client requests a bin or sensor that does not exist? What status code do you return and why?**

Ans:



**RQ5: Where does your API read its data from? Trace the path of event data from the PIR sensor all the way to an API response.**

Ans:



**RQ6: What query parameters does your events endpoint support? Show an example request and response.**

Ans:



**RQ7: How do the Flask-RESTx models (api.model) relate to the Swagger UI documentation? What happens in the UI when you add a new field to a model?**

Ans:



**RQ8: Show a screenshot of your Swagger UI with endpoints visible.**

Ans:



**RQ9: Explain how the POST /mqtt/publish endpoint works. What does the API do when it receives a publish request?**

Ans:



**RQ10: You published a motion event through the API using POST /mqtt/publish. Describe the full path that message takes, from the HTTP request to the consumer’s JSONL file.**

Ans:



**RQ11: What does GET /mqtt/topics return? Why does the API need to subscribe to smartbin/# for this to work?**

Ans:



**RQ12: You call POST /bins/bin-01/emptied. This both saves a record and publishes to MQTT. What is the advantage of combining both actions in one endpoint?**

Ans:



**RQ13: What is AsyncAPI and how does it relate to OpenAPI? Why do you need both for the Smart Wastebin?**

Ans:



**RQ14: How many channels did you document in your AsyncAPI spec? For each, state who is the publisher and who is the subscriber.**

Ans:



**RQ15: Show a screenshot of your AsyncAPI spec rendered in Swagger Editor or AsyncAPI Studio.**

Ans:



**RQ16: Compare the MotionEvent message schema in your AsyncAPI spec with the event_model in your Flask-RESTx code. They describe the same data, what is different about the context in which each is used?**

Ans:



**RQ17: Show the curl command and response for: (a) listing all bins, (b) getting events with a limit, (c) publishing an MQTT message, (d) requesting a nonexistent bin.**

Ans:



**RQ18: What is the difference between testing with Swagger UI and testing with curl? When would you use each?**

Ans:



**RQ19: A new team member joins your project. They need to build a mobile app that shows bin status and lets users report full bins. What do you hand them? How do the Swagger UI and AsyncAPI spec help?**

Ans:



**RQ20: In your own words, explain why the Smart Wastebin needs both a push-based system (MQTT) and a pull-based system (REST API). What would be missing if you only had one?**

Ans:



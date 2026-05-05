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


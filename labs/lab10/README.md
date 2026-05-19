# Lab 09 — Data Processing on Edge Devices

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
- **OUT** -> Pin 11 (GPIO17 / Physical Pin 11)

### Environment Setup / Activation (venv)
Navigate to the `labs/lab09` directory:
```bash
cd raspberryPiProject/labs/lab09
```

### Dependency Installation
Install the required packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Prerequisites: MQTT Broker
Ensure you have a running MQTT broker (e.g., Mosquitto). You can check its status:
```bash
sudo systemctl status mosquitto
```

### Running the System

To run the complete pipeline, open four separate terminals in the `labs/lab09` directory:

1. **Terminal 1: Start the Producer**
   ```bash
   python producer.py --pin 11
   ```
   *Reads the physical PIR sensor and publishes events to MQTT.*

2. **Terminal 2: Start the Consumer**
   ```bash
   python consumer.py --verbose
   ```
   *Listens for events and saves them to `data/` logs.*

3. **Terminal 3: Start the Rule-based Virtual Sensor**
   ```bash
   python virtual_sensor_rules.py --broker localhost --subscribe-topic "smartbin/bin-01/pir-01/events" --publish-topic smartbin/bin-01/usage --window 10 --interval 10
   ```
   *Analyzes real-time motion frequency to determine usage levels (idle, low, medium, high).*

4. **Terminal 4: Start the ML Virtual Sensor**
   First, train the model (if not already done):
   ```bash
   python train_model.py
   ```
   Then, run the ML sensor:
   ```bash
   python virtual_sensor_ml.py --broker localhost --publish-topic smartbin/bin-01/prediction --interval 60
   ```
   *Predicts the bin's usage level for the next hour using a Random Forest classifier.*

### Monitoring MQTT Traffic
You can verify the messages being published by subscribing to all smartbin topics:
```bash
mosquitto_sub -h localhost -t "smartbin/#" -v
```


---

## Section B: Report

**RQ1: How does Node-RED differ from writing a Python script? What is the “unit of work” in each? (In Python it is a function or a class. In Node-RED it is…?)**

Ans: Node-RED differs from writing a Python script primarily in its event-driven, visual programming model versus Python’s linear, text-based execution.  While Python scripts execute top-to-bottom as a single process, Node-RED operates as a runtime environment where flows (collections of interconnected nodes) manage asynchronous message passing between modular components. 



**RQ2: What is the Node-RED message object? What is msg.payload and why does every node use it?**

Ans:



**RQ3: What does the Deploy button do? Why do you need to click it after making changes?**

Ans:



**RQ4: Show a screenshot of your usage monitor flow. Label each node and explain what it does.**

Ans:



**RQ5: In the counting Function node, you might have used flow.set and flow.get. What do these do? How is this similar to and different from a Python variable?**

Ans:



**RQ6: How does the Switch node compare to a Python if statement? What advantages does the visual version have?**

Ans:



**RQ7: You built a branching flow (count → publish + alert if high). In Python, this would be an if-else block. In Node-RED, it is visible wiring. Which is easier to understand at a glance? Which is easier to test?**

Ans:



**RQ8: Your Python consumer and your Node-RED flow both subscribe to the same MQTT topic. How is this possible? Do they interfere with each other?**

Ans:



**RQ9: You could build the usage monitor as a Python script (Lab 09) or as a Node-RED flow (this lab). Compare the two approaches: lines of code vs number of nodes, ease of modification, ease of testing, who can work with each.**

Ans:



**RQ10: Could Node-RED replace your Python producer (the script that reads the PIR sensor)? Why or why not?**

Ans:



**RQ11: Where does Node-RED fit in your overall system architecture? Draw or describe how it sits alongside the producer, consumer, Home Assistant, and REST API.**

Ans:



**RQ12: A facilities manager (non-programmer) wants to add a new rule: “if no motion is detected for 6 hours during business hours, mark the bin as possibly blocked.” Could they build this in Node-RED without help? What nodes would they need?**

Ans:



**RQ13: What are the limitations of Node-RED that the lecture mentioned? Did you encounter any of them in this lab?**

Ans:



**RQ14: You exported your flows as flows.json. A teammate imports it into their Node-RED instance. What will they need to configure manually? (Hint: think about the MQTT broker connection.)**

Ans:



**RQ15: Compare flows.json with a Python script in terms of version control. If two teammates edit the flow at the same time, what happens when they try to merge?**

Ans:



**RQ16: After building the same logic in Python (Lab 09) and Node-RED (this lab), which did you find faster to build? Which would you trust more in production? Why?**

Ans:



**RQ17: The lecture argued that low-code platforms let more people contribute to the system. After this lab, do you agree? Who in your project team could use Node-RED that could not write the Python equivalent?**

Ans:



**RQ18: If you were designing the Smart Wastebin system from scratch, which parts would you build in Python and which in Node-RED? Explain your reasoning.**

Ans:



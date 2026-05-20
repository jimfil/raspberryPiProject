# Lab 10 — Node-RED LCDP

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
   python producer.py --pin 4
   ```
   *Reads the physical PIR sensor and publishes events to MQTT.*

2. **Open the Node-RED editor by navigating to [pi's:IP_ADDRESS]:1880**


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

Ans: The Node-RED message object is a JSON object that is passed between nodes in a flow. It has a payload property that contains the data that is being passed between the nodes. Every node in Node-RED uses the payload property to receive and send data.  The reason every node uses it is for convienence and standatization.  



**RQ3: What does the Deploy button do? Why do you need to click it after making changes?**

Ans: The Deploy button takes that visual draft, compiles it into a functional JSON configuration, and sends it to the background Node.js server to be actively executed. We need to click it because the visual interface that we build our logic in, is separate from the runtime environment.



**RQ4: Show a screenshot of your usage monitor flow. Label each node and explain what it does.**

Ans: ![stage3.png](labs/lab10/screenshots/stage3.png)
**Node Descriptions:**

* **MQTT In (`.../motion`):** Subscribes to and receives motion events from the bin's PIR sensor.
* **Switch 1:** Filters incoming messages, allowing only actual motion detections to pass through.
* **File (`detected_events.log`):** Logs and saves the valid motion events to a local file.
* **Function 1:** Processes the data (e.g., calculates total bin usage) and formats the final payload.
* **MQTT Out (`.../usage/nodered`):** Publishes the processed usage data to the MQTT broker.
* **Dashboard Nodes (`le` & `bin usage`):** Visualize the usage level on the Node-RED UI using both text and a gauge chart.
* **Debug & Switch 2:** Auxiliary nodes used for troubleshooting the flow and inspecting output data.



**RQ5: In the counting Function node, you might have used flow.set and flow.get. What do these do? How is this similar to and different from a Python variable?**

Ans: In Node-RED, `flow.set()` and `flow.get()` are used to store and retrieve variables that persist for the entire duration of the flow. We used them to keep track of the number of motion events and the last time motion was detected.



**RQ6: How does the Switch node compare to a Python if statement? What advantages does the visual version have?**

Ans: The Switch node in Node-RED is used to control the flow of messages based on a set of conditions. It is similar to an if statement in Python, but it is a visual representation of the conditional logic and we can represent the many `if...else` statements in a simple block.



**RQ7: You built a branching flow (count → publish + alert if high). In Python, this would be an if-else block. In Node-RED, it is visible wiring. Which is easier to understand at a glance? Which is easier to test?**

Ans: The branching flow in Node-RED is easier to understand at a glance because we can see the flow of messages and the conditions that control it. It is also easier to test because we can test each node individually and see the output of each node via the debug nodes.



**RQ8: Your Python consumer and your Node-RED flow both subscribe to the same MQTT topic. How is this possible? Do they interfere with each other?**

Ans: Since they only subscribe to the topic, they dont interfere with each other at all. If they were both publishing to the same topic, then they would likely intefere with each other.



**RQ9: You could build the usage monitor as a Python script (Lab 09) or as a Node-RED flow (this lab). Compare the two approaches: lines of code vs number of nodes, ease of modification, ease of testing, who can work with each.**

Ans: We found the node red flow much easier to build and modify, but only because we are familiar with JS. Otherwise Python would be our go to choice.



**RQ10: Could Node-RED replace your Python producer (the script that reads the PIR sensor)? Why or why not?**

Ans: Yes, Node-RED can replace our python producer, firstly because Node-RED has native rpi-gpio input nodes for sensors. Secondly, the implementation of publiching to the MQTT broker can be implemented very quickly and easily.



**RQ11: Where does Node-RED fit in your overall system architecture? Draw or describe how it sits alongside the producer, consumer, Home Assistant, and REST API.**

Ans: Node-RED acts as an intermediary processing and automation layer within our event-driven architecture, sitting on the same tier as the Python consumer, Home Assistant, and the REST API when it comes to subscribing to the MQTT broker. 
- **Producer**: Reads hardware sensors (PIR) and publishes raw events to the MQTT broker.
- **MQTT Broker**: The central hub that routes messages.
- **Node-RED**: Subscribes to the raw events from the broker, applies business logic (e.g., counting, filtering, alerting), and can publish processed metrics back to the broker or trigger external services.
- **Home Assistant**: Subscribes to the broker for home automation and dashboards, receiving both raw events from the producer and processed states/metrics from Node-RED.
- **Python Consumer / REST API**: The consumer listens to the broker to log data for persistence, which the REST API then exposes for external queries. Node-RED can also directly query this API using HTTP request nodes if historical data is needed.



**RQ12: A facilities manager (non-programmer) wants to add a new rule: “if no motion is detected for 6 hours during business hours, mark the bin as possibly blocked.” Could they build this in Node-RED without help? What nodes would they need?**

Ans: Yes, a non-programmer could likely build this in Node-RED with minimal training because of its intuitive visual interface and pre-built nodes, avoiding the need to write complex Python timing logic. They would primarily need the following nodes:
- **MQTT In node**: To subscribe to the bin's motion events.
- **Time Range (or Switch) node**: To filter messages so the logic only applies during business hours (e.g., 9 AM to 5 PM).
- **Trigger node**: This is the key node for this task. It can be configured to send a message if it does *not* receive a new message for 6 hours. Any new motion event received resets the 6-hour timer.
- **MQTT Out (or Debug/Email) node**: To publish the "possibly blocked" alert to a dashboard or send a notification once the Trigger node fires.



**RQ13: What are the limitations of Node-RED that the lecture mentioned? Did you encounter any of them in this lab?**

Ans: We had a difficulty working in Node-RED at the same time for the lab, since resolving merge conflicts in it is difficult.



**RQ14: You exported your flows as flows.json. A teammate imports it into their Node-RED instance. What will they need to configure manually? (Hint: think about the MQTT broker connection.)**

Ans: When a teammate imports the `flows.json` file, they will need to manually configure environment-specific configuration nodes. Most importantly, they will need to update the **MQTT Broker connection settings** to point to their own MQTT broker's IP address or hostname (e.g., `localhost` or their Raspberry Pi's IP). Furthermore, for security reasons, Node-RED does not export credentials (like usernames and passwords) within `flows.json`. Therefore, if the MQTT broker or any other external service requires authentication, the teammate will need to manually re-enter those credentials.



**RQ15: Compare flows.json with a Python script in terms of version control. If two teammates edit the flow at the same time, what happens when they try to merge?**

Ans: Python scripts are line-based and modular, making them very friendly to version control systems like Git. If two developers edit different parts of a Python file, Git can typically merge the changes automatically. If a conflict does occur, the differences are in readable code and relatively easy to resolve manually.

In contrast, `flows.json` is a single, large JSON array containing the entire layout, node configurations, generated IDs, and connections (wiring). If two teammates edit the flow at the same time, Git will likely see massive structural changes in the JSON file. Trying to merge these changes usually results in complex merge conflicts that are extremely difficult for a human to read and resolve manually without breaking the JSON structure. Often, teams are forced to discard one person's work and manually recreate the changes in the Node-RED visual editor.



**RQ16: After building the same logic in Python (Lab 09) and Node-RED (this lab), which did you find faster to build? Which would you trust more in production? Why?**

Ans: Node-RED was easier and we built the same logic faster in it than Python. In production, if we had to choose which one to use, we would pick Node-RED, not only because it is easier to use for a non-programmer, the node structure makes it easier to debug and fix pre and post production.



**RQ17: The lecture argued that low-code platforms let more people contribute to the system. After this lab, do you agree? Who in your project team could use Node-RED that could not write the Python equivalent?**

Ans: Truth is, it was actually harder but quicker, since all the members of our team know how to write python code, but only one member knows JavaScript, the language the code was written in, but the Python code required more effort.



**RQ18: If you were designing the Smart Wastebin system from scratch, which parts would you build in Python and which in Node-RED? Explain your reasoning.**

Ans: We would probably build all the publish-subscribe relations to Node-RED, meaning the producer and the consumer too, because it is much faster and easier to impement than in Python, and it also handles asynchronous events greatly, meaning the pub-sub model.



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
- **OUT** -> Pin 11 (GPIO17)

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
You need a running MQTT broker (e.g., Mosquitto). On a Raspberry Pi, it usually runs as a service. You can check its status:
```bash
sudo systemctl status mosquitto
```

### Running the System

To run the complete pipeline, open three separate terminals in the `labs/lab08` directory:

1. **Terminal 1: Start the API**
   ```bash
   python api.py
   ```
   *Note: The API dynamically loads bins and sensors from the `models/` directory.*

2. **Terminal 2: Start the Consumer**
   ```bash
   python consumer.py --sensor_id urn:dev:team05:pir-01
   ```
   *The consumer will listen for events and save them to `data/pir-01_events.log`.*

3. **Terminal 3: Start the Producer**
   ```bash
   python producer.py --bin_id bin-01 --sensor_id pir-01
   ```
   *The producer will read the physical PIR sensor and publish events to MQTT.*

### Accessing the Documentation
Once the API is running, you can view the interactive Swagger UI at:
`http://<your-pi-ip>:5000/`


---

## Section B: Report

**RQ1: What thresholds did you use for idle/low/medium/high? How did you decide on these values?**

Ans:



**RQ2: What window size did you choose and why? What happens if you make it too short (e.g., 1 minute) or too long (e.g., 60 minutes)?**

Ans:



**RQ3: How does the rolling window implementation (the deque) relate to what the lecture described as CEP windowed operators?**

Ans:



**RQ4: What would you need to change if you wanted to add a new level (e.g., “critical” for bins that might overflow)?**

Ans:



**RQ5: What features did you use for the classifier? Why these features?**

Ans:



**RQ6: Show the classification report from training. What is the accuracy? Which class (busy/quiet) is harder to predict?**

Ans:



**RQ7: Why did we use a Random Forest classifier? Could you use a different model? What would change?**

Ans:



**RQ8: The training data is synthetic. What would change if you used real motion data collected over several weeks? What patterns might emerge that the synthetic data misses?**

Ans:



**RQ9: The model publishes a confidence score alongside the prediction. Why is this useful? What should a consumer do if confidence is low (e.g., 55%)?**

Ans:



**RQ10: Give one scenario where the rule-based sensor and the ML sensor disagree. Which one would you trust more in that scenario, and why?**

Ans:



**RQ11: The rule-based sensor reacts to the present. The ML sensor predicts the future. Give one use case where each is more useful.**

Ans: The rule-based sensor would prove more useful if we have a random day in which a lot of people use the smart bin in, let's say a public area, and it detects when the bin is full or close to full. The ML sensor would prove useful in a situation where we have a smart bin or bins in a more controlled environment like an office building where the sensor has gathered enough data to predict when a bin is going to be full, or in which area, taking into account the working hours and office spaces the workers primarily have.



**RQ12: If motion patterns changed tomorrow (e.g., the bin was moved to a new location), which sensor would adapt first? What would you need to do for the other?**

Ans: The rule-based sensor would adapt first because it acts independently and it doesn't need data of the area and time beforehand like  the ML sensor.



**RQ13: You added two new processing components to your system without modifying the producer or consumer. How did the pub/sub architecture make this possible?**

Ans:



**RQ14: Both virtual sensors publish to MQTT. Could a third virtual sensor subscribe to their output and combine them? Give an example.**

Ans:



**RQ15: Show a screenshot with the raw motion sensor, usage intensity, and activity prediction all visible.**

Ans:



**RQ16: In the DIKW pyramid, where does the raw motion event sit? Where does the usage level sit? Where does the prediction sit? What moved the data up each level?**

Ans:



**RQ17: In your own words, what is a virtual sensor? How does it differ from a physical sensor?**

Ans:



**RQ18: If you had access to additional sensors (temperature, fill level, noise), what virtual sensor could you build by combining them? Describe the inputs, the logic, and the output.**

Ans:



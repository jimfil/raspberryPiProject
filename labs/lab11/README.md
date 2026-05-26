# Lab 11 — Data Visualization for the Smart Wastebins

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



**RQ1: Include a screenshot of your Lab 07 dashboard and your redesigned dashboard side by side. What are the three biggest improvements?**

Ans:


**RQ2: How did you implement information hierarchy? What is at the top of your dashboard and why?**

Ans:


**RQ3: How does your dashboard handle a sensor going offline? Show what the user sees.**

Ans:

**RQ4: Does your dashboard show overview first, zoom and filter, details on demand? Describe each level.**

Ans:

**RQ5: Test your dashboard on a narrow screen (resize the browser to phone width). Does it still work? What breaks?**

Ans:

**RQ6: For all your charts. For each chart, state: (a) what question it answers, (b) why you chose that chart type, (c) one insight the chart reveals.**

Ans:

**RQ7: Which two additional charts did you create beyond the five provided? Why did you choose those visualizations?**

Ans:

**RQ8: Look at your heatmap (hour × day of week). What patterns do you see? Do they match what you expected?**

Ans:

**RQ9: Look at your latency distribution. Is it symmetric or skewed? Are there outliers? What could cause them?**

Ans:

**RQ10: Apply RUSTIC to one of your Seaborn charts. Rate it on each criterion and identify one thing you would improve.**

Ans:

**RQ11: Compare your Home Assistant dashboard and your Seaborn charts. Give one question that each answers better than the other.**

Ans:

**RQ12: A facilities manager and a data analyst both need information from your system. Which visualization tool would you give each, and why?**

Ans:

**RQ13: Could you embed your Seaborn charts into Home Assistant? How? Would it make sense to do so?**

Ans:

**RQ14: Which RUSTIC criterion was hardest to achieve in your Home Assistant dashboard? Why?**

Ans:

**RQ15: You showed your redesigned dashboard to a classmate who has never seen the system. Could they understand it without explanation? What did they find confusing (if anything)?**

Ans:

**RQ16: In your own words, what is the difference between a dashboard that shows data and a dashboard that supports decisions?**

Ans:


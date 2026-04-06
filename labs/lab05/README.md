# Lab 05 — Context-aware Data Modeling

## Section A: Code / Runbook

### Repository structure

```
lab05/
├── models/
│   ├── context.jsonld
│   ├── sensor.jsonld
│   ├── wastebin.jsonld
│   └── environment.jsonld
├── run_pipeline.py
├── requirements.txt
└── README.md
```

### How to run the pipeline

```bash
# 1. Create & activate virtualenv
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline (on the Raspberry Pi)
python run_pipeline.py \
  --device-id  pir-01 \
  --pin        7 \
  --sample-interval 0.1 \
  --cooldown   5.0 \
  --min-high   0.5 \
  --queue-size 64 \
  --duration   60 \
  --out        motion_output.jsonl \
  --verbose
```
### How the pipeline produces self-describing output

`run_pipeline.py` loads `models/context.jsonld` on startup and inlines the `@context` in **every** JSONL record. Each observation also carries `@type: "sosa:Observation"` plus three entity references (`sensor_ref`, `wastebin_ref`, `environment_ref`) that point back to the model files via their `@id` URIs.

**Example output line** (pretty-printed):

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn": "http://www.w3.org/ns/ssn/",
    "saref": "https://saref.etsi.org/core/",
    "bot": "https://w3id.org/bot#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "schema": "https://schema.org/",
    "pipeline": "https://github.com/jimfil/raspberryPiProject/blob/main/docs/ontology.md#",
    "event_time": {"@id": "sosa:resultTime", "@type": "xsd:dateTime"},
    "device_id": {"@id": "sosa:madeBySensor", "@type": "@id"},
    "event_type": "@type",
    "motion_state": "pipeline:motionState",
    "seq": {"@id": "pipeline:sequenceNumber", "@type": "xsd:integer"},
    "run_id": {"@id": "pipeline:runId", "@type": "xsd:string"},
    "ingest_time": {"@id": "pipeline:ingestTime", "@type": "xsd:dateTime"},
    "pipeline_latency_ms": {"@id": "pipeline:pipelineLatencyMs", "@type": "xsd:float"},
    "sensor_ref": {"@id": "pipeline:sensorRef", "@type": "@id"},
    "wastebin_ref": {"@id": "pipeline:wastebinRef", "@type": "@id"},
    "environment_ref": {"@id": "pipeline:environmentRef", "@type": "@id"}
  },
  "@type": "sosa:Observation",
  "device_id": "urn:dev:team05:pir-01",
  "sensor_ref": "urn:dev:team05:pir-01",
  "wastebin_ref": "urn:wastebin:bin-01",
  "environment_ref": "urn:env:kypes-02",
  "event_time": "2026-04-10T14:32:01.123Z",
  "event_type": "motion",
  "motion_state": "detected",
  "seq": 7,
  "run_id": "d1f3a2b4-5678-9abc-def0-123456789abc",
  "ingest_time": "2026-04-10T14:32:01.130Z",
  "pipeline_latency_ms": 7.0
}
```

---

### JSON-LD Models

#### `models/sensor.jsonld`

```json
{
  "@context": "context.jsonld",
  "@id": "urn:dev:team05:pir-01",
  "@type": "sosa:Sensor",
  "name": "HC-SR501 PIR Motion Sensor",
  "description": "HC-SR501 passive infrared (PIR) motion sensor mounted on wastebin bin-01 in the lab environment. Detects motion by sensing changes in infrared radiation emitted by warm bodies within its detection cone.",
  "manufacturer": "Generic / HICHIP",
  "model": "HC-SR501",
  "sosa:observes": "sosa:Motion",
  "ssn:detects": "Changes in infrared radiation from warm bodies (humans) moving within the detection cone",
  "pipeline:gpioPin": 7,
  "pipeline:operatingVoltage": "5V DC",
  "pipeline:detectionRange": "up to 7 metres",
  "pipeline:detectionAngle": "less than 120 degrees cone",
  "pipeline:cooldownSeconds": 5.0,
  "pipeline:minHighSeconds": 0.5,
  "pipeline:operatingTemperature": "-15°C to +70°C",
  "pipeline:indoorOutdoor": "indoor",
  "pipeline:mountedOn": { "@id": "urn:wastebin:bin-01" },
  "pipeline:deployedIn": { "@id": "urn:env:kypes-02" },
  "installationDate": "2026-03-31",
  "pipeline:statusSensor": "active",
  "identifier": "pir-01"
}
```

#### `models/wastebin.jsonld`

```json
{
  "@context": "context.jsonld",
  "@id": "urn:wastebin:bin-01",
  "@type": "saref:Appliance",
  "name": "Smart Wastebin Unit 01",
  "description": "An IoT-enabled outdoor waste collection bin located in kypes-02, University of Patras. Equipped with a PIR motion sensor to detect deposit activity.",
  "pipeline:capacityLt": 0.48,
  "pipeline:material": "HDPE plastic",
  "pipeline:color": "grey,blue",
  "pipeline:lengthCm": 6.5,
  "pipeline:widthCm": 7,
  "pipeline:heightCm": 14.5,
  "pipeline:wasteType": "general",
  "pipeline:collectionZone": "Ground Level of ECE Building",
  "pipeline:collectionRoute": "Classrooms 6-8, CCCS 1-3(kypes aithouses)",
  "pipeline:statusBin": "active",
  "sosa:hosts": [{ "@id": "urn:dev:team05:pir-01" }],
  "pipeline:locatedIn": { "@id": "urn:env:kypes-02" },
  "identifier": "bin-01",
  "installationDate": "2026-03-31"
}
```

#### `models/environment.jsonld`

```json
{
  "@context": "context.jsonld",
  "@id": "urn:env:kypes-02",
  "@type": "bot:Space",
  "name": "kypes-02",
  "description": "kypes-02, Department of Electrical and Computer Engineering, University of Patras, Greece.",
  "pipeline:university": "University of Patras",
  "pipeline:department": "Electrical and Computer Engineering",
  "pipeline:roomName": "kypes",
  "pipeline:roomNumber": 2,
  "pipeline:buildingName": "Engineering Building A",
  "pipeline:floorNumber": 0,
  "address": { "addressLocality": "Patras", "addressCountry": "GR" },
  "pipeline:indoorOutdoor": "indoor",
  "pipeline:trafficLevel": "medium",
  "pipeline:contains": [
    { "@id": "urn:wastebin:bin-01" },
    { "@id": "urn:dev:team05:pir-01" }
  ]
}
```

#### `models/context.jsonld`

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn": "http://www.w3.org/ns/ssn/",
    "saref": "https://saref.etsi.org/core/",
    "bot": "https://w3id.org/bot#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "schema": "https://schema.org/",
    "pipeline": "https://github.com/jimfil/raspberryPiProject/blob/main/docs/ontology.md#",
    "event_time": { "@id": "sosa:resultTime", "@type": "xsd:dateTime" },
    "device_id": { "@id": "sosa:madeBySensor", "@type": "@id" },
    "event_type": "@type",
    "motion_state": "pipeline:motionState",
    "seq": { "@id": "pipeline:sequenceNumber", "@type": "xsd:integer" },
    "run_id": { "@id": "pipeline:runId", "@type": "xsd:string" },
    "ingest_time": { "@id": "pipeline:ingestTime", "@type": "xsd:dateTime" },
    "pipeline_latency_ms": { "@id": "pipeline:pipelineLatencyMs", "@type": "xsd:float" },
    "sensor_ref": { "@id": "pipeline:sensorRef", "@type": "@id" },
    "wastebin_ref": { "@id": "pipeline:wastebinRef", "@type": "@id" },
    "environment_ref": { "@id": "pipeline:environmentRef", "@type": "@id" }
  }
}
```

### Entity-Relationship Diagram

![alt text](images/image.png)
> **Figure 1 — Data-model entity-relationship diagram.**  Four entities participate in the model: the **PIR Sensor** (`sosa:Sensor`), the **Wastebin** (`saref:Appliance`), the **Environment** (`bot:Space`), and each **Observation** (`sosa:Observation`) emitted by the pipeline.
---
## Section B: Report

**RQ1: Which vocabularies/ontologies did you use across your models? Why did you choose them over alternatives?**

Ans:



**RQ2: What properties did you include in your sensor description? Which ones came from standard vocabularies and which ones did you define yourself?**

Ans:



**RQ3: What properties did you include in your wastebin description? How did you decide what to include and what to leave out?**

Ans:



**RQ4: How did you model the relationships between sensor, wastebin, and environment? Show the relevant @id references from each JSON-LD file.**

Ans:



**RQ5: Were there properties you wanted to include but could not find a standard term for? How did you handle them?**

Ans:

**RQ6: Show your complete @context and explain each mapping. For each field, why did you choose that particular standard term (or why did you define a custom one)?**

Ans:



**RQ7: How did you define your custom namespace? What URL did you use and why?**

Ans:



**RQ8: Take one field from your old pipeline output (e.g., event_time). What did it mean before? What does it mean now that it is mapped to a standard term? What is the practical difference?**

Ans:



**RQ9: What is the role of @context in JSON-LD? What happens if you remove it is the JSON still valid? Is it still self-describing?**

Ans:



**RQ10: How did you handle the @context in your streaming JSONL pipeline, inline, external reference, or something else? What are the trade-offs of your choice?**

Ans:

**RQ11: Include your entity-relationship diagram in the report. Explain the diagram briefly, what are the entities, what are the key relationships, and how does an observation connect to the rest of the model?**

Ans:

**RQ12: Another team uses a different motion sensor (e.g., microwave radar instead of PIR) but follows the same JSON-LD context. Could a downstream application process both teams’ data without modification? Why or why not?**

Ans:



**RQ13: You need to add an ultrasonic distance sensor to measure bin fill level. What new JSON-LD files would you create? What would you change in existing files? What would stay the same?**

Ans:



**RQ14: What properties are missing from your models that a real-world deployment would need? Name at least three and explain why they matter.**

Ans:



**RQ15: Look at one domain-specific data model repository (e.g., SAREF, Smart Data Models, SSN). Find a model related to waste management, sensors, or smart buildings. How does it compare to what you built?**

Ans:

**RQ16: In the DIKW pyramid from the lecture, where does your raw Lab 03 JSONL output sit? Where does the JSON-LD version sit? What moved it up the pyramid?**

Ans:



**RQ17: In your own words, what is the difference between data that works and data that communicates information?**

Ans:



**RQ18: If you had to explain to a non-technical person why your pipeline now produces “better” data, what would you say?**

Ans:
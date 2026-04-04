# Smart Wastebin — Custom Ontology Terms

Base namespace: `https://github.com/jimfil/raspberryPiProject/blob/main/docs/ontology.md#`
Prefix used in JSON-LD: `pipeline`

## Entity Types

The JSON-LD model files (`sensor.jsonld`, `wastebin.jsonld`, `environment.jsonld`) contain only instance data (plain key-value pairs). The RDF types for each entity are defined here.

### urn:dev:team05:pir-01
- **Model File:** `sensor.jsonld`
- **RDF Type:** `sosa:Sensor`
- **Description:** HC-SR501 PIR motion sensor

### urn:wastebin:bin-01
- **Model File:** `wastebin.jsonld`
- **RDF Type:** `saref:Appliance`
- **Description:** Smart wastebin unit

### urn:env:kypes-02
- **Model File:** `environment.jsonld`
- **RDF Type:** `bot:Space`
- **Description:** Deployment environment (room/space)

### Detection stimulus (nested in sensor)
- **RDF Type:** `ssn:Stimulus`
- **Description:** Changes in infrared radiation from warm bodies detected by the PIR sensor

### University (nested in environment)
- **RDF Type:** `schema:Organization`
- **Description:** The university where the system is deployed

### Department (nested in environment)
- **RDF Type:** `schema:Organization`
- **Description:** The department within the university

### Address (nested in environment)
- **RDF Type:** `schema:PostalAddress`
- **Description:** Postal address of the university

---

## Event Context Terms

The following terms are aliased in `context.jsonld` for pipeline events. Their expected datatypes are defined here.

### event_time
- **Type:** `xsd:dateTime`
- **Description:** Timestamp of the event

### device_id
- **Type:** `@id` (IRI reference)
- **Description:** The sensor that produced the event

### event_type
- **Type:** `@type`
- **Description:** RDF type of the event

### motion_state
- **Type:** `xsd:string`
- **Description:** Motion state (e.g., HIGH / LOW)

### seq
- **Type:** `xsd:integer`
- **Description:** Sequence number of the event

### run_id
- **Type:** `xsd:string`
- **Description:** Identifier for the pipeline run

### ingest_time
- **Type:** `xsd:dateTime`
- **Description:** Time the event was ingested

### pipeline_latency_ms
- **Type:** `xsd:float`
- **Description:** Pipeline processing latency in ms

---

## Pipeline Terms

### gpioPin
- **Type:** `xsd:integer`
- **Description:** The GPIO pin number on the Raspberry Pi that the sensor is connected to.

### operatingVoltage
- **Type:** `xsd:string`
- **Description:** The required voltage for the sensor to operate.

### detectionRange
- **Type:** `xsd:string`
- **Description:** The physical range within which the sensor can successfully trigger.

### cooldownSeconds
- **Type:** `xsd:float`
- **Description:** The hardware cooldown period before detecting another event.

### detectionAngle
- **Type:** `xsd:string`
- **Description:** The angle of the cone of detection for the sensor.

### minHighSeconds
- **Type:** `xsd:float`
- **Description:** The minimum seconds the signal stays high when triggered.

### operatingTemperature
- **Type:** `xsd:string`
- **Description:** The safe temperature range for sensor operation.

### indoorOutdoor
- **Type:** `xsd:string`
- **Description:** Indicates whether the deployment is suited for indoor or outdoor.

### statusSensor
- **Type:** `xsd:string`
- **Description:** Administrative tracking of the sensor status (e.g., active).

### mountedOn
- **Type:** `owl:ObjectProperty`
- **Description:** A relationship indicating what physical object a sensor is attached to.

### deployedIn
- **Type:** `owl:ObjectProperty`
- **Description:** A relationship indicating the environment in which the system is deployed.

### locatedIn
- **Type:** `owl:ObjectProperty`
- **Description:** A relationship indicating that a device or physical object is physically located in a certain environment.

### capacityLt
- **Type:** `xsd:float`
- **Description:** The capacity of the wastebin in liters.

### material
- **Type:** `xsd:string`
- **Description:** The material of the wastebin.

### color
- **Type:** `xsd:string`
- **Description:** The color of the wastebin.

### lengthCm
- **Type:** `xsd:float`
- **Description:** The length of the wastebin in centimeters.

### widthCm
- **Type:** `xsd:float`
- **Description:** The width of the wastebin in centimeters.

### heightCm
- **Type:** `xsd:float`
- **Description:** The height of the wastebin in centimeters.

### wasteType
- **Type:** `xsd:string`
- **Description:** The type of waste the wastebin is designed to collect.

### collectionZone
- **Type:** `xsd:string`
- **Description:** The zone where the wastebin is located.

### collectionRoute
- **Type:** `xsd:string`
- **Description:** The route for collecting waste from the wastebin.

### statusBin
- **Type:** `xsd:string`
- **Description:** Administrative tracking of the wastebin status (e.g., active,full, maintenance).

### university
- **Type:** `xsd:string`
- **Description:** A relationship indicating the university where the system is deployed.

### department
- **Type:** `xsd:string`
- **Description:** A relationship indicating the department where the system is deployed.

### roomName
- **Type:** `xsd:string`
- **Description:** A relationship indicating the room where the system is deployed.

### roomNumber
- **Type:** `xsd:integer    `
- **Description:** A relationship indicating the room number where the system is deployed.

### buildingName
- **Type:** `xsd:string`
- **Description:** A relationship indicating the building where the system is deployed.

### floorNumber
- **Type:** `xsd:integer`
- **Description:** A relationship indicating the floor number where the system is deployed.

### indoorOutdoor
- **Type:** `xsd:string`
- **Description:** Indicates whether the deployment is suited for indoor or outdoor.

### trafficLevel
- **Type:** `xsd:string`
- **Description:** Indicates the traffic level of the environment.

### contains
- **Type:** `owl:ObjectProperty`
- **Description:** A relationship indicating that an environment contains a device or physical object.


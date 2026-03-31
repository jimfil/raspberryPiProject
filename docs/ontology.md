# Smart Wastebin — Custom Ontology Terms

Base namespace: `https://github.com/jimfil/raspberryPiProject/blob/main/docs/ontology.md#`
Prefix used in JSON-LD: `pipeline`

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


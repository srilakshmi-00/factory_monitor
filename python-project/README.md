# Factory Machine Health Monitoring System

## Introduction

This project is a **Factory Machine Health Monitoring System** built in Python. It models a factory with multiple machines, each equipped with sensors for **Temperature**, **Pressure**, and **Vibration**. The system loads sensor data from a CSV file, computes the health of each machine using a specific formula, and generates alerts for critical failures or missing sensors.

**Health Formula:**

```
health = 100 - (temperature / 2 + pressure / 10 + vibration * 20)
```

**Alert Rules:**
- If health < 50: `Critical Machine Failure Risk`
- If any required sensor is missing: `Sensor Offline Warning`

---

## Explanation of Classes

### Sensor
- **Attributes:**
	- `id`: Unique sensor identifier
	- `type`: Sensor type (`"Temperature"`, `"Pressure"`, `"Vibration"`)
	- `reading`: Numeric value from the sensor
- **Methods:**
	- Properties for each attribute

### Machine
- **Attributes:**
	- `id`: Unique machine identifier
	- `sensors`: Dictionary of attached sensors by type
- **Methods:**
	- `add_sensor(sensor)`: Attach a sensor to the machine
	- `compute_health()`: Calculates health using the formula; tracks missing sensors
	- `missing_sensors`: List of missing required sensor types

### FactoryMonitor
- **Attributes:**
	- `machines`: Dictionary of all machines in the factory
- **Methods:**
	- `add_machine(machine)`: Add a machine to the factory
	- `check_machines()`: Returns health and alerts for each machine

### main.py
- Loads sensor data from a CSV file
- Creates sensors and machines
- Uses `FactoryMonitor` to compute health and print alerts

---

## Example Input/Output

### Example Input (CSV: `data.csv`)

```csv
machine_id,sensor_id,sensor_type,reading
M1,S1,Temperature,60
M1,S2,Pressure,100
M1,S3,Vibration,2
M2,S4,Temperature,70
M2,S5,Pressure,110
M3,S6,Temperature,80
M3,S7,Pressure,120
```

### Example Output

```
Machine M1: Health=16.50 | Status=Critical Machine Failure Risk
Machine M2: Health=10.00 | Status=Critical Machine Failure Risk
Machine M3: Health=None | Status=Sensor Offline Warning: Vibration
```
# Python Project for Factory Monitoring System

This project implements a factory monitoring system that tracks the health of machines using various sensors. The system is designed to manage multiple machines, each equipped with different types of sensors, and to detect any anomalies in their health status.

## Project Structure

```
python-project
├── src
│   ├── sensor.py
│   ├── machine.py
│   ├── factory_monitor.py
│   └── main.py
└── README.md
```

## Files Description

- **src/sensor.py**: Defines the `Sensor` class, which represents a sensor with a unique identifier, type, and current reading.

- **src/machine.py**: Defines the `Machine` class, which holds multiple sensors and computes the overall health of the machine based on the readings from its sensors.

- **src/factory_monitor.py**: Defines the `FactoryMonitor` class, which manages multiple machines and checks for any anomalies in their health status.

- **src/main.py**: The entry point of the application, which includes functions to load sensor data from a CSV file and print the health status of each machine.

## Setup Instructions

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Ensure you have Python installed on your machine.
4. Install any required dependencies (if applicable).

## Usage Examples

- To create sensors and machines, instantiate the `Sensor` and `Machine` classes from the `sensor.py` and `machine.py` files respectively.
- Use the `FactoryMonitor` class to manage multiple machines and check for anomalies in their health.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.
import csv
from sensor import Sensor
from machine import Machine
from factory_monitor import FactoryMonitor

def load_data_from_csv(csv_file):
    machines = {}
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None or not all(field in reader.fieldnames for field in ['machine_id', 'sensor_id', 'sensor_type', 'reading']):
                raise ValueError("Malformed CSV: Missing required columns.")
            for row in reader:
                m_id = row['machine_id']
                s_id = row['sensor_id']
                s_type = row['sensor_type']
                try:
                    reading = float(row['reading'])
                except (ValueError, TypeError):
                    raise ValueError(f"Malformed CSV: Invalid reading value in row {row}")
                if m_id not in machines:
                    machines[m_id] = Machine(m_id)
                machines[m_id].add_sensor(Sensor(s_id, s_type, reading))
        if not machines:
            raise ValueError("CSV file is empty or contains no valid data.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        exit(1)
    return machines

def print_machine_health(machines):
    monitor = FactoryMonitor()
    for m in machines.values():
        monitor.add_machine(m)
    results = monitor.check_machines()
    for m_id, (health, alerts) in results.items():
        print(f"Machine {m_id} Health: {health:.2f}")
        for alert in alerts:
            print(f"  ALERT: {alert}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <data.csv>")
        sys.exit(1)
    machines = load_data_from_csv(sys.argv[1])
    print_machine_health(machines)

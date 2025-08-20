from sensor import Sensor


class Machine:
    REQUIRED_TYPES = ["Temperature", "Pressure", "Vibration"]

    def __init__(self, id):
        self.id = id
        self.sensors = {}

    def add_sensor(self, sensor):
        self.sensors[sensor.type] = sensor

    def compute_health(self):
        warnings = []
        readings = {}
        for t in self.REQUIRED_TYPES:
            if t in self.sensors:
                readings[t] = self.sensors[t].reading
            else:
                readings[t] = 0
                warnings.append("Sensor Offline Warning")
        temp = readings["Temperature"]
        pressure = readings["Pressure"]
        vibration = readings["Vibration"]
        health = 100 - (temp / 2 + pressure / 10 + vibration * 20)
        return health, warnings

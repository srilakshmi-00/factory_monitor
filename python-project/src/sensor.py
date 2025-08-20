
class Sensor:
    def __init__(self, sensor_id, sensor_type, reading):
        self._id = sensor_id
        self._type = sensor_type
        self._reading = reading

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def reading(self):
        return self._reading



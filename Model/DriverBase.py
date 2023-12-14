from Model.LocalDataStorage import LocalDataStorage
from Model.Sensors.SensorBase import SensorBase


class DriverBase:
    def __init__(self, name):
        self.name = name
        self.storage = LocalDataStorage()
        self.relative_speed_change = (0, 0)

    def get_speed_change(self, car_sensor: SensorBase, track_sensor: SensorBase):
        self.relative_speed_change = (0, 0)
        self._think(car_sensor, track_sensor)
        return self.relative_speed_change

    def _think(self, car_sensor: SensorBase, track_sensor: SensorBase):
        raise NotImplementedError()

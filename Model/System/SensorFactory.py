from Model.System.ServiceContainer import ServiceContainer


class SensorFactory:
    def __init__(self,
                 car_sensor_type,
                 track_sensor_type,
                 service_container: ServiceContainer
                 ):
        self._car_sensor_type = car_sensor_type
        self._track_sensor_type = track_sensor_type
        self._service_container = service_container

    def create_car_sensor(self, c):
        if self._car_sensor_type is None:
            return None

        self._service_container.update(c)
        return self._car_sensor_type(self._service_container)

    def create_track_sensor(self):
        if self._track_sensor_type is None:
            return None

        return self._track_sensor_type(self._service_container)

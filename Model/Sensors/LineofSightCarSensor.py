from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor
from Model.System.ServiceContainer import ServiceContainer


class LineOfSightCarSensor(CarSensor):
    def __init__(self, service_container: ServiceContainer):
        super().__init__(service_container)
        self.__path_sensor = service_container.get_first(LineSensor)

    def line_of_sight(self, end_coordinates):
        return self.__path_sensor.is_path_homogeneous(
            self.__car.get_position(),
            end_coordinates)

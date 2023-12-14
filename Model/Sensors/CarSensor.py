from Model.Car import Car
from Model.System.ServiceContainer import ServiceContainer


class CarSensor:
    def __init__(self, service_container: ServiceContainer):
        self.__car = service_container.get_first(Car)

    def get_iteration(self):
        return self.__car.get_step_count()

    def get_position(self):
        return self.__car.get_position_reversed_time(0)

    def get_speed(self):
        return self.__car.get_speed()

    def is_restarting(self):
        return self.__car.is_restarting()

    def get_speed_vector_length(self):
        return self.__car.get_speed_vector_length()

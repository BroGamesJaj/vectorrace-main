from Model.Sensors.SensorBase import SensorBase
from Model.System.ServiceContainer import ServiceContainer


class LimitedSensor(SensorBase):
    MAX_READS = 0

    def __init__(self, service_container: ServiceContainer, limit_reads: bool = True):
        super().__init__(service_container)
        self.__read_counter = 0
        self.__limit_reads = limit_reads
        self.__car = None

    def can_scan(self):
        return not self.__limit_reads or self.__read_counter < LimitedSensor.MAX_READS

    def _scan(self):
        if self.__limit_reads:
            self.__read_counter += 1

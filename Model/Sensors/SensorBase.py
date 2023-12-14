from Model.System.ServiceContainer import ServiceContainer
from Model.Track import Track


class SensorBase:
    def __init__(self, service_container: ServiceContainer):
        self._track = service_container.get_first(Track)

    def get_track_size(self):
        return self._track.get_size()

    def get_start_direction(self):
        return self._track.get_start_direction()

    def can_scan(self):
        return True

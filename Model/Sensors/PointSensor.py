from Model.Sensors.LimitedSensor import LimitedSensor
from Model.Sensors.Results.PointOnMapResult import PointOnMapResult
from Model.Sensors.Results.PointOnTrackResult import PointOnTrackResult


class PointSensor(LimitedSensor):

    def is_point_on_track(self, coordinate):
        if self.can_scan():
            self._scan()
            return PointOnTrackResult(coordinate, self._track.get_point(coordinate) == 0)
        else:
            return None

    def is_point_on_map(self, coordinate):
        if self.can_scan():
            self._scan()
            return PointOnMapResult(
                coordinate,
                self._track.is_point_on_map(coordinate)
            )
        else:
            return None

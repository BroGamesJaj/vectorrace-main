from Model.Sensors.Results.PathCheckResult import PathCheckResult
from Model.Sensors.PointSensor import PointSensor


class PathSensorBase(PointSensor):
    def is_path_homogeneous(self, start_coordinate, end_coordinate):
        if self.can_scan():
            self._scan()
            path = self._get_path(
                        start_coordinate[0], start_coordinate[1],
                        end_coordinate[0], end_coordinate[1]
                    )
            return PathCheckResult(
                start_coordinate, end_coordinate, path,
                self._track.get_point(start_coordinate) == 0,
                self._track.get_point(end_coordinate) == 0,
                self._track.check_path(path)
            )
        else:
            return None

    def _get_path(self, r0, c0, r1, c1):
        raise NotImplementedError()

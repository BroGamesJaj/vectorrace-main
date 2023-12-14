from Model.Sensors.Results.SensorResultBase import SensorResultBase


# Public data members:
# + start_coordinate: tuple - the start coordinate of path (row, column)
# + end_coordinate: tuple - the end coordinate of path (row, column)
# + path: list of tuples - list of coordinates (row, column) between start and end coordinates
#           the path is calculated by _get_path method inherited from the PathSensorBase class
# + is_start_on_track: bool - is first coordinate on track
# + is_end_on_track: bool - is last coordinate on track
# + last_on_track: tuple - last coordinate of path on track
class PathCheckResult(SensorResultBase):
    def __init__(self,
                 start_coord, end_coord, path,
                 is_start_on_track: bool, is_end_on_track: bool,
                 last_same_as_start
                 ):
        self.start_coordinate = start_coord
        self.end_coordinate = end_coord
        self.path = path
        self.is_start_on_track = is_start_on_track
        self.is_end_on_track = is_end_on_track
        self.last_same_as_start = last_same_as_start

    def __str__(self):
        return "{0}-{1}->{2}..{3}..{4}?{5}".format(
            self.start_coordinate, self.end_coordinate,
            self.is_start_on_track, len(self.path), self.last_same_as_start, self.is_end_on_track
        )

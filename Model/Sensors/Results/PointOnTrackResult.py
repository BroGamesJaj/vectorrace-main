from Model.Sensors.Results.SensorResultBase import SensorResultBase


# Public data members:
# + coordinate: tuple - the evaluated coordinate (row, column)
# + is_on_track: bool - is coordinate on track

class PointOnTrackResult(SensorResultBase):
    def __init__(self, coord, is_on_track: bool):
        self.coordinate = coord
        self.is_on_track = is_on_track

    def __str__(self):
        return "{0}->{1}".format(self.coordinate, self.is_on_track)

from Model.Sensors.Results.SensorResultBase import SensorResultBase


# Public data members:
# + coordinate: tuple - the evaluated coordinate (row, column)
# + is_on_track: bool - is coordinate on track

class PointOnMapResult(SensorResultBase):
    def __init__(self, coord, is_on_map: bool):
        self.coordinate = coord
        self.is_on_map = is_on_map

    def __str__(self):
        return "{0}->{1}".format(self.coordinate, self.is_on_map)

import math

from Model.DriverBase import DriverBase
from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor


class Driver_32(DriverBase):

    def _think(self, car_sensor: CarSensor, track_sensor: LineSensor):
        # default inputs
        pos_y, pos_x = car_sensor.get_position()
        speed_y, speed_x = car_sensor.get_speed()
        speed_vector_length = car_sensor.get_speed_vector_length()
        iteration = car_sensor.get_iteration()

        # custom values from the storage to local variables
        is_first_run = self.storage.get("first_run", True)
        total_length = self.storage.get("total_length", 0)

        # use local variables
        total_length += math.sqrt(speed_y ** 2 + speed_x ** 2)
        if is_first_run:
            print("Track size: {0}".format(track_sensor.get_track_size()))

        # update custom values in the storage
        self.storage.set("first_run", False)
        self.storage.set("total_length", total_length)

        # set output, default in each call: (0, 0)
        # for now, as a test, continuous acceleration in start direction
        self.relative_speed_change = track_sensor.get_start_direction()

        next_position = (
            pos_y + speed_y + self.relative_speed_change[0],
            pos_x + speed_x + self.relative_speed_change[1]
        )

        # test sensor read limit (sensor returns -1 if read limit reached)
        while track_sensor.can_scan():
            # sensor returns: PointOnTrackResult object
            # PointOnTrackResult.is_on_track: bool - is coordinate on track
            sensor_value = track_sensor.is_point_on_track(next_position)
            print(
                iteration,
                pos_y, pos_x,
                total_length,
                speed_y, speed_x, speed_vector_length,
                sensor_value
            )

            if sensor_value.is_on_track:
                # move forward
                pass
            else:
                # turn
                pass


    def get_breaking_point(self, max_corner_speed, current_speed):
        braking_point = (current_speed - max_corner_speed)
        return braking_point

    def can_speed_up(self, braking_point, corner_pos, current_pos):
        dist = math.sqrt(abs(current_pos[0] - corner_pos[0]) ** 2 + abs(current_pos[1] - corner_pos[1]) ** 2)
        if dist > braking_point:
            return True
        else:
            return False
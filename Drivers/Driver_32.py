import math

from Model.DriverBase import DriverBase
from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor


class Driver_32(DriverBase):

    def _think(self, car_sensor: CarSensor, track_sensor: LineSensor):
        # default inputs
        track_width = self.storage.get("track_width", [0, 0])
        start_direction = self.storage.get("start_direction", [0, 0])
        map_size = self.storage.get("map_size",[0,0])
        speed_y, speed_x = 0, 0
        pos_y, pos_x = car_sensor.get_position()
        is_first_run = self.storage.get("first_run", True)
        iteration = self.storage.get("iteration",0)
        if is_first_run:
            print("first run")
            self.storage.set("iteration", 1)
            map_size = track_sensor.get_track_size()
            self.storage.set("map_size",map_size)
            start_direction = track_sensor.get_start_direction()
            self.storage.set("start_direction", start_direction)
            track_width = track_sensor.is_path_homogeneous((pos_y, pos_x), (
            abs(map_size[0] * start_direction[0]), abs(map_size[1] * start_direction[1])))
            track_width = abs(track_width.last_same_as_start[0] - pos_y), abs(track_width.last_same_as_start[1] - pos_x)
            track_width = (track_width[0] + track_width[1]) * 2
            self.storage.set("track_width", track_width)


        if not is_first_run and not iteration == 2:
            iteration += 1
            self.storage.set("iteration",iteration)
            speed_y, speed_x = car_sensor.get_speed()
            speed_vector_length = car_sensor.get_speed_vector_length()
        if iteration == 2:
            self.storage.set("iteration", iteration+1)
            print("second run")
            print(self.get_corner(start_direction, 0, (pos_y, pos_x), True, track_sensor, map_size, track_width))

        # custom values from the storage to local variables
        is_first_run = self.storage.get("first_run", True)
        total_length = self.storage.get("total_length", 0)

        # use local variables
        total_length += math.sqrt(speed_y ** 2 + speed_x ** 2)

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
            """ print(
                iteration,
                pos_y, pos_x,
                total_length,
                speed_y, speed_x, speed_vector_length,
                sensor_value
            ) """

            if sensor_value.is_on_track:
                # move forward
                pass
            else:
                # turn
                pass

    def get_corner(self, direction, prev_corner_in_dir, apex_or_edge, edge, track_sensor, map_size, track_width):
        if edge:
            line1 = track_sensor.is_path_homogeneous((apex_or_edge[0], apex_or_edge[1]),
                                                     (abs(map_size[0] * direction[0]), abs(map_size[1] * direction[1])))

            if direction == [0, -1]:
                line2_start = apex_or_edge[0] + 2 + track_width, apex_or_edge[1]
            elif direction == [1, 0]:
                line2_start = apex_or_edge[1] + 2 + track_width, apex_or_edge[0]
            elif direction == [0, 1]:
                line2_start = apex_or_edge[0] - 2 - track_width, apex_or_edge[1]
            else:
                line2_start = apex_or_edge[1] - 2 - track_width, apex_or_edge[0]
            line2 = track_sensor.is_path_homogeneous((line2_start[0], line2_start[1]),
                                                     (abs(map_size[0] * direction[0]), abs(map_size[1] * direction[1])))
            if abs(line1.last_same_as_start[0] - apex_or_edge[0]) + abs(line1.last_same_as_start[1] - apex_or_edge[1]) - abs(line2.last_same_as_start[0] - line2_start[0]) + abs(line2.last_same_as_start[1] - line2_start[1]) > 0:

                if direction[0] == 0 and direction[1] == -1:
                    return [line1.last_same_as_start[0] + 1, line1.last_same_as_start[1] - 1], direction, (-1, 0)
                elif direction[0] == 1 and direction[1] == 0:
                    return [line1.last_same_as_start[0] + 1, line1.last_same_as_start[1] + 1], direction, (0, -1)
                elif direction[0] == -1 and direction[1] == 0:
                    return [line1.last_same_as_start[0] - 1, line1.last_same_as_start[1] - 1], direction, (0, 1)
                elif direction[0] == 0 and direction[1] == 1:
                    return [line1.last_same_as_start[0] - 1, line1.last_same_as_start[1] + 1], direction, (1, 0)
            else:
                if direction[0] == 0 and direction[1] == -1:
                    return [line2.last_same_as_start[0] - 1, line2.last_same_as_start[1] - 1], (1, 0)
                elif direction[0] == 1 and direction[1] == 0:
                    return [line2.last_same_as_start[0] + 1, line2.last_same_as_start[1] - 1], (0, 1)
                elif direction[0] == -1 and direction[1] == 0:
                    return [line2.last_same_as_start[0] - 1, line2.last_same_as_start[1] + 1], (0, -1)
                elif direction[0] == 0 and direction[1] == 1:
                    return [line2.last_same_as_start[0] + 1, line2.last_same_as_start[1] + 1], (-1, 0)
        else:
            start_pos = 0
            if direction == [0, -1] and prev_corner_in_dir == [1, 0]:
                start_pos = apex_or_edge[0] - 1, apex_or_edge[1] - 1
            elif direction == [0, -1] and prev_corner_in_dir == [-1, 0]:
                start_pos = apex_or_edge[0] + 1, apex_or_edge[1] - 1
            elif direction == [0, 1] and prev_corner_in_dir == [1, 0]:
                start_pos = apex_or_edge[0] - 1, apex_or_edge[1] + 1
            elif direction == [0, 1] and prev_corner_in_dir == [-1, 0]:
                start_pos = apex_or_edge[0] + 1, apex_or_edge[1] + 1
            elif direction == [1, 0] and prev_corner_in_dir == [0, 1]:
                start_pos = apex_or_edge[0] + 1, apex_or_edge[1] - 1
            elif direction == [1, 0] and prev_corner_in_dir == [0, -1]:
                start_pos = apex_or_edge[0] + 1, apex_or_edge[1] + 1
            elif direction == [-1, 0] and prev_corner_in_dir == [0, 1]:
                start_pos = apex_or_edge[0] - 1, apex_or_edge[1] - 1
            elif direction == [-1, 0] and prev_corner_in_dir == [0, 1]:
                start_pos = apex_or_edge[0] - 1, apex_or_edge[1] + 1

            line1 = track_sensor.is_path_homogeneous((start_pos[0], start_pos[1]),
                                                     (abs(map_size[0] * direction[0]), abs(map_size[1] * direction[1])))
            if direction == [0, -1]:
                line2_start = start_pos[0] + 2 + track_width, start_pos[1]
            elif direction == [1, 0]:
                line2_start = start_pos[1] + 2 + track_width, start_pos[0]
            elif direction == [0, 1]:
                line2_start = start_pos[0] - 2 - track_width, start_pos[1]
            else:
                line2_start = start_pos[1] - 2 - track_width, start_pos[0]
            line2 = track_sensor.is_path_homogeneous((line2_start[0], line2_start[1]),
                                                     (abs(map_size[0] * direction[0]), abs(map_size[1] * direction[1])))

            if abs(line1.last_same_as_start[0] - apex_or_edge[0]) + abs(line1.last_same_as_start[1] - apex_or_edge[1]) - abs(line2.last_same_as_start[0] - line2_start[0]) + abs(line2.last_same_as_start[1] - line2_start[1]) > 0:
                if direction[0] == 0 and direction[1] == -1:
                    return [line1.last_same_as_start[0] + 1, line1.last_same_as_start[1] - 1], direction, [-1, 0]
                elif direction[0] == 1 and direction[1] == 0:
                    return [line1.last_same_as_start[0] + 1, line1.last_same_as_start[1] + 1], direction, [0, -1]
                elif direction[0] == -1 and direction[1] == 0:
                    return [line1.last_same_as_start[0] - 1, line1.last_same_as_start[1] - 1], direction, [0, 1]
                elif direction[0] == 0 and direction[1] == 1:
                    return [line1.last_same_as_start[0] - 1, line1.last_same_as_start[1] + 1], direction, [1, 0]
            else:
                if direction[0] == 0 and direction[1] == -1:
                    return [line2.last_same_as_start[0] - 1, line2.last_same_as_start[1] - 1], [1, 0]
                elif direction[0] == 1 and direction[1] == 0:
                    return [line2.last_same_as_start[0] + 1, line2.last_same_as_start[1] - 1], [0, 1]
                elif direction[0] == -1 and direction[1] == 0:
                    return [line2.last_same_as_start[0] - 1, line2.last_same_as_start[1] + 1], [0, -1]
                elif direction[0] == 0 and direction[1] == 1:
                    return [line2.last_same_as_start[0] + 1, line2.last_same_as_start[1] + 1], [-1, 0]

    def get_braking_point(self, max_corner_speed, current_speed):
        braking_point = (current_speed - max_corner_speed)
        return braking_point

    def can_speed_up(self, braking_point, corner_pos, current_pos):
        dist = math.sqrt(abs(current_pos[0] - corner_pos[0]) ** 2 + abs(current_pos[1] - corner_pos[1]) ** 2)
        if dist > braking_point:
            return True
        else:
            return False

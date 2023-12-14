from Model.DriverBase import DriverBase
from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor


class TestDriver2(DriverBase):

    def _think(self, car_sensor: CarSensor, track_sensor: LineSensor):
        # default inputs
        pos_y, pos_x = car_sensor.get_position()
        speed_y, speed_x = car_sensor.get_speed()
        speed_vector_length = car_sensor.get_speed_vector_length()
        iteration = car_sensor.get_iteration()
        is_first_run = self.storage.get("first_run", True)
        self.storage.set("first_run", False)

        if is_first_run and max(abs(speed_y), abs(speed_x)) == 0:
            self.relative_speed_change = track_sensor.get_start_direction()

        next_position = (
            pos_y + speed_y + self.relative_speed_change[0],
            pos_x + speed_x + self.relative_speed_change[1]
        )

        point_check_value = track_sensor.is_point_on_track(next_position)
        path_check_value = track_sensor.is_path_homogeneous((pos_y, pos_x), next_position)

        if not point_check_value.is_on_track or not path_check_value.is_end_on_track:
            self.relative_speed_change = (-speed_y, -speed_x)

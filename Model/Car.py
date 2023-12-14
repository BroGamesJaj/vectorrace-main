import math
import random

import numpy as np

from queue import Queue

from Model.DriverBase import DriverBase


class Car:
    speed_change_max = 1
    speed_value_converter = None

    position_limits = None

    restart_min = 10
    restart_max = 14

    def __init__(self,
                 driver: DriverBase,
                 initial_position, color):
        self._driver = driver
        self._current_position = initial_position
        self._speed = np.zeros(len(initial_position)).astype(int)
        self._state = 1
        self._positions = [initial_position.copy()]
        self._stopped = 0
        self._driver_errors = 0
        self._step_count = 0
        self._restarting = 0
        self.color = color

    def stopped(self):
        self._state = 2

    def timed_out(self):
        self._state = 3

    def run_off_track(self):
        self._state = 4

    def run_off_map(self):
        self._state = 5

    def driver_error(self):
        self._state = 6

    def restart(self):
        print("Restarting car of {0}".format(self.get_driver_name()))
        self._restarting = random.randint(Car.restart_min, Car.restart_max)

    def set_current_position(self, new_location):
        del self._positions[0]
        self._current_position = list(new_location)
        self._positions.insert(0, self._current_position.copy())
        self._speed = np.zeros(self._speed.shape).astype(int)

    def add_steps(self, new_steps):
        self._step_count += new_steps

    def get_state(self):
        return self._state

    def is_running(self):
        return self._state == 1

    def is_restarting(self):
        return self._restarting > 0

    def is_stopped(self):
        return self._state == 2

    def is_timed_out(self):
        return self._state == 3

    def get_driver_name(self):
        return self._driver.name

    def get_driver_type(self):
        return type(self._driver).__name__

    def get_position_count(self):
        return len(self._positions)

    def get_position_reversed_time(self, index=0):
        if index >= len(self._positions):
            return None
        return self._positions[index]

    def get_position(self, index, return_last: bool = False):
        if index < 0:
            return None

        if len(self._positions) <= index:
            if return_last:
                return self._positions[0]
            else:
                return None

        return self._positions[len(self._positions) - 1 - index]

    def get_speed(self):
        return self._speed.copy()

    def get_step_count(self):
        return self._step_count

    def get_stopped(self):
        return self._stopped

    def get_driver_errors(self):
        return self._driver_errors

    def get_speed_vector_length(self):
        return math.sqrt(self._speed[0] ** 2 + self._speed[1] ** 2)

    def get_restarting(self):
        return self._restarting

    @staticmethod
    def _validate_speed_modifier_value(v):
        if abs(v) > Car.speed_change_max:
            v = Car.speed_change_max * v / abs(v)

        if Car.speed_value_converter is not None:
            v = Car.speed_value_converter(v)

        return v

    def drive(self, input_queue: Queue):
        car_sensor = input_queue.get()
        track_sensor = input_queue.get()

        try:
            self._driver.get_speed_change(car_sensor, track_sensor)
        except Exception as ex:
            print("Driver ({0}) error: {1}".format(self._driver.name, ex))
            self._driver_errors += 1

    def limit_speed(self, max_speed):
        speed_angle = math.atan2(self._speed[0], self._speed[1])
        self._speed[0] = int(round(min(self.get_speed_vector_length(), max_speed) * math.sin(speed_angle)))
        self._speed[1] = int(round(min(self.get_speed_vector_length(), max_speed) * math.cos(speed_angle)))

    def update(self):
        if self._restarting > 0:
            self._restarting -= 1
            self._positions.insert(0, self._current_position.copy())
            return True

        speed_delta = [Car._validate_speed_modifier_value(v) for v in list(self._driver.relative_speed_change)]

        for i in range(self._speed.shape[0]):
            self._speed[i] += speed_delta[i]

        self._current_position += self._speed

        is_valid = (0 <= self._current_position[0] < Car.position_limits[0]
                    and 0 <= self._current_position[1] < Car.position_limits[1])
        if self._current_position[0] < 0:
            self._current_position[0] = 0
        if Car.position_limits is not None and self._current_position[0] >= Car.position_limits[0]:
            self._current_position[0] = Car.position_limits[0] - 1
        if self._current_position[1] < 0:
            self._current_position[1] = 0
        if Car.position_limits is not None and self._current_position[1] >= Car.position_limits[1]:
            self._current_position[1] = Car.position_limits[1] - 1

        self._positions.insert(0, self._current_position.copy())

        return is_valid

    def speed_check(self):
        if self.get_speed_vector_length() == 0:
            if not self.is_restarting():
                self._stopped += 1
        else:
            self._stopped = 0

    def __str__(self):
        return "Driver: {0} at {1} Speed: {2}+{3} in state: {4} [R{5};S{6};E{7}]".format(
            self._driver.name, self._current_position,
            self._speed, self._driver.relative_speed_change,
            self._state,
            self._restarting, self._stopped, self._driver_errors
        )

    def serialize_positions(self) -> str:
        serialized_text = ";".join(["{0}, {1}".format(p[0], p[1]) for p in self._positions])
        return "{0};{1}".format(self._driver.name, serialized_text)

    def deserialize_positions(self, serialized_text: str):
        positions = serialized_text.split(";")
        self._driver.name = positions[0]
        self._positions = []
        for pi in range(1, len(positions)):
            coords = positions[pi].split(",")
            self._positions.append((int(coords[0]), int(coords[1])))

import time

from queue import Queue

from Model.Car import Car
from Model.DriverLog import DriverLog
from Model.LinearAlgebra import LinearAlgebra
from Model.System.Logging.Logger import Logger
from Model.System.SensorFactory import SensorFactory
from Model.Sensors.LimitedSensor import LimitedSensor
from Model.System.ServiceContainer import ServiceContainer
from Model.Track import Track
from Model.Sensors.LineSensor import LineSensor


class Race:
    def __init__(self,
                 service_container: ServiceContainer,
                 cars: [Car],
                 sensor_factory: SensorFactory,
                 max_sensor_reads_per_iteration: int,
                 max_iterations: int,
                 max_stopped_iterations: int, max_driver_errors: int,
                 max_think_seconds: float,
                 can_leave_track: bool,
                 restart_on_leaving_track: bool,
                 off_track_speed_limit: int
                 ):
        self._track = service_container.get_first(Track)
        self._logger = service_container.get_first(Logger)
        self._can_leave_track = can_leave_track
        self._restart_on_leaving_track = restart_on_leaving_track
        self._off_track_speed_limit = off_track_speed_limit
        self._on_track_sensor = LineSensor(service_container, limit_reads=False)
        self._cars = cars
        self._driver_logs = []
        for c in self._cars:
            self._driver_logs.append(DriverLog(c.get_driver_name()))

        self._sensor_factory = sensor_factory
        self._max_sensor_read_count = max_sensor_reads_per_iteration
        self._max_iterations = max_iterations
        self._max_stopped_iterations = max_stopped_iterations
        self._max_driver_errors = max_driver_errors
        self._max_think_seconds = max_think_seconds

    def get_driver_logs(self):
        return self._driver_logs

    def run(self):
        LimitedSensor.MAX_READS = self._max_sensor_read_count
        DriverLog.SPLIT_COUNT = self._track.get_split_count()

        iteration = 1
        active_cars = 1

        while iteration <= self._max_iterations and active_cars > 0:
            self._logger.log("Iteration: {0}".format(iteration), 5)

            active_cars = 0
            for c in self._cars:
                if c.is_running() > 0:
                    active_cars += 1
                    # thread safe parameter passing
                    queue = Queue()
                    queue.put(self._sensor_factory.create_car_sensor(c))
                    queue.put(self._sensor_factory.create_track_sensor())

                    start_time = time.time()
                    c.drive(queue)
                    end_time = time.time()

                    if 0 < self._max_think_seconds < end_time - start_time:
                        c.timed_out()

                        self._log(
                            iteration, c,
                            "Driver: {0} thought {1:.3f}s TIMED OUT".format(
                                c.get_driver_name(), end_time - start_time
                            )
                        )

            for c in self._cars:
                if c.is_running() > 0:
                    is_valid = c.update()
                    c.add_steps(1)

                    car_on_track = self._on_track_sensor.is_point_on_track(c.get_position_reversed_time())
                    if not car_on_track.is_on_track:
                        wall_info = self._on_track_sensor.is_path_homogeneous(
                            c.get_position_reversed_time(1),
                            c.get_position_reversed_time()
                        )

                        if self._can_leave_track:
                            if wall_info.is_start_on_track and self._restart_on_leaving_track:
                                c.restart()
                            c.limit_speed(self._off_track_speed_limit)
                        else:
                            c.set_current_position(wall_info.last_same_as_start)
                            if wall_info.is_start_on_track and self._restart_on_leaving_track:
                                c.restart()

                    c.speed_check()
                    self._get_driver_log_line(c.get_driver_name()).set_speed(c.get_speed_vector_length())

                    if self._check_split(c):
                        self._log(
                            iteration, c,
                            "crossed checkpoint {0}".format(
                                self._track.get_split(
                                    self._get_driver_log_line(c.get_driver_name()).get_next_split_index()
                                ).name
                            )
                        )
                        self._get_driver_log_line(c.get_driver_name()).add_split(iteration)

                    if c.get_stopped() > self._max_stopped_iterations:
                        c.stopped()
                        self._log(iteration, c, " stopped")

                    if (not self._can_leave_track and not car_on_track.is_on_track
                            and not self._restart_on_leaving_track):
                        c.run_off_track()
                        self._log(iteration, c, " run off the track")

                    if not is_valid:
                        c.run_off_map()
                        self._log(iteration, c, " run off the MAP")

                    if c.get_driver_errors() > self._max_driver_errors:
                        c.driver_error()
                        self._log(iteration, c, " driver failed to drive")

                    self._logger.log(str(c), 5)

            iteration += 1

    def _get_driver_log_line(self, driver_identifier):
        for d in self._driver_logs:
            if d.get_identifier() == driver_identifier:
                return d
        return None

    def _check_split(self, car):
        return LinearAlgebra.check_incision_of_sections(
            (car.get_position_reversed_time(1), car.get_position_reversed_time(0)),
            self._track.get_split(self._get_driver_log_line(car.get_driver_name()).get_next_split_index()).vector
        )

    def _log(self, iteration: int, car: Car, event: str, log_level: int = 4):
        if self._logger is not None:
            self._logger.log(
                "In iteration #{0} {1} {2}".format(iteration, car.get_driver_name(), event),
                log_level
            )

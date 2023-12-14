from datetime import datetime
import importlib.util
import os
import sys

from Model.System.Logging.ConsoleLogChannel import ConsoleLogChannel
from Model.System.Logging.DateDecorator import DateDecorator
from Model.System.Logging.FileLogChannel import FileLogChannel
from Model.System.Logging.Logger import Logger
from Model.System.Logging.TimeDecorator import TimeDecorator
from Model.System.SensorFactory import SensorFactory
from Model.Sensors.CarSensor import CarSensor
from Model.Sensors.LineSensor import LineSensor
from Model.System.ServiceContainer import ServiceContainer
from Model.System.Settings import Settings
from Model.Visualizer.AnimationVisualizer import AnimationVisualizer
from Model.Car import Car
from Model.Visualizer.ColorSource import ColorSource
from Model.Visualizer.ImageVisualizer import ImageVisualizer
from Model.Race import Race
from Model.Track import Track


def select_track(folder_name):
    track_files = os.listdir(folder_name)

    track_list = []
    for full_name in track_files:
        file_name, extension = os.path.splitext(full_name)
        if extension == '.yml' or extension == ".yaml":
            track_list.append((file_name, extension))

    print("Available tracks:")
    for i in range(len(track_list)):
        print("{0}: {1}".format(i, track_list[i][0]))

    if len(track_list) > 1:
        print("You can set a default track name using TrackName/TN command line parameter!")
        selected_track = int(input("Select track index: "))
    else:
        selected_track = 0

    if selected_track < 0:
        selected_track = 0
    if selected_track >= len(track_list):
        selected_track = len(track_list) - 1

    return (r"{0}\{1}{2}".format(folder_name, track_list[selected_track][0], track_list[selected_track][1]),
            "{0}{1}".format(track_list[selected_track][0], track_list[selected_track][1])
            )


def lazy_import(class_name):
    spec = importlib.util.find_spec(class_name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[class_name] = module
    loader.exec_module(module)
    return module


def create_cars(folder_name):
    driver_files = os.listdir(folder_name)

    car_list = []
    for f in driver_files:
        file_name, extension = os.path.splitext(f)
        if extension == '.py':
            car_list.append(
                Car(
                    driver=getattr(lazy_import("Drivers.{0}".format(file_name)), file_name)(file_name),
                    initial_position=track.get_start(),
                    color=color_source.get_next_color()
                )
            )
    return car_list


def log_results(race_to_log: Race, race_logger: Logger):
    race_to_log.get_driver_logs().sort(
        key=lambda x: (x.get_splits_crossed(), -x.get_last_split_iteration()),
        reverse=True
    )
    race_logger.log("\n========== Drivers by distance and time ==========", 4)
    for dl in race_to_log.get_driver_logs():
        race_logger.log(str(dl), 4)

    race_to_log.get_driver_logs().sort(
        key=lambda x: x.get_max_speed(),
        reverse=True
    )
    race_logger.log("\n========== Drivers by max speed ==========", 4)
    for dl in race_to_log.get_driver_logs():
        race_logger.log(str(dl), 4)


def write_car_coords_to_files(track_name, track_file, result_folder, car_list):
    with open(
            r"{0}\{1}_{2}.coords".format(
                result_folder,
                track_name, datetime.now().strftime("%Y%m%d_%H%M%S")
            ),
            "w") as text_file:
        text_file.write("{0}\n".format(track_file))
        for c in car_list:
            text_file.write(c.serialize_positions() + "\n")


if __name__ == '__main__':
    expected_argument_count = 6
    if len(sys.argv) != expected_argument_count:
        print("Command line arguments: "
              "TF:<track descriptor YAML folder> DF:<folder of drivers> LF:<log_folder> "
              "LT:<Log type: None/Events/Coords/Both> V:<visualization type: Animated/Still>")

    settings = Settings(sys.argv)

    track_folder = settings.get_parameter_by_key("TracksFolder", "Tracks")
    if settings.get_parameter_by_key("TrackName", None) is None:
        track_descriptor = select_track(track_folder)
    else:
        track_descriptor = (
            r"{0}\{1}".format(track_folder, settings.get_parameter_by_key("TrackName")),
            settings.get_parameter_by_key("TrackName")
        )
    driver_folder = settings.get_parameter_by_key("DriversFolder", "Drivers")
    log_folder = settings.get_parameter_by_key("LogsFolder", "Logs")
    log_into_file = settings.get_parameter_by_key("LogType", "none").lower() in ["events", "both"]
    save_car_coords = settings.get_parameter_by_key("LogType", "none").lower() in ["coords", "both"]
    visualization_type = settings.get_parameter_by_key("VisualizationType", "Animated")

    logger = Logger(log_level=5)
    logger.add_channel(ConsoleLogChannel(log_level=4))
    if log_into_file:
        logger.add_channel(
            TimeDecorator(
                DateDecorator(
                    FileLogChannel(
                        r"{0}\Race_{1}.log".format(log_folder, datetime.now().strftime("%Y%m%d%H%M%S")),
                        log_level=5
                    )
                )
            )
        )

    logger.log("Track descriptor: {0}".format(track_descriptor[0]), 4)

    track = Track(track_descriptor[0])

    service_container = ServiceContainer()
    service_container.append(track)
    service_container.append(LineSensor(service_container))
    service_container.append(logger)

    Car.speed_change_max = 1
    Car.speed_value_converter = lambda x: int(x)
    Car.position_limits = track.get_size()
    Car.restart_min = 4
    Car.restart_max = 8
    color_source = ColorSource()

    cars = create_cars(driver_folder)

    if len(cars) == 0:
        print("There is no driver specified!")
        exit()

    race = Race(
        service_container,
        cars=cars,
        sensor_factory=SensorFactory(CarSensor, LineSensor, service_container),
        max_sensor_reads_per_iteration=5,
        max_iterations=500,
        max_stopped_iterations=10,
        max_driver_errors=10,
        max_think_seconds=-1,
        can_leave_track=False, restart_on_leaving_track=True,
        off_track_speed_limit=2
    )

    stats = race.run()

    log_results(race, logger)

    if save_car_coords:
        write_car_coords_to_files(track.get_name(), track_descriptor[1], log_folder, cars)

    if visualization_type.lower() == "still":
        visualizer = ImageVisualizer(
            track=track,
            track_image=track.get_track(), down_sample=1,
            cars=cars, path_color_coefficient=0.6
        )
        visualizer.create_image()
        visualizer.show_image()

    if visualization_type.lower() == "animated":
        visualizer = AnimationVisualizer(
            track=track,
            track_image=track.get_track(), down_sample=1,
            cars=cars, path_color_coefficient=0.6,
            track_log_length=3,
            repeat=1
        )
        visualizer.show_animation(100)

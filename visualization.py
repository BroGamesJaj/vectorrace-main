import os
import sys

from Model.DriverBase import DriverBase
from Model.System.Settings import Settings
from Model.Visualizer.AnimationVisualizer import AnimationVisualizer
from Model.Car import Car
from Model.Visualizer.ColorSource import ColorSource
from Model.Visualizer.ImageVisualizer import ImageVisualizer
from Model.Track import Track


def select_log(folder_name):
    track_files = os.listdir(folder_name)

    log_list = []
    for full_name in track_files:
        file_name, extension = os.path.splitext(full_name)
        if extension == '.coords':
            log_list.append((file_name, extension))

    print("Available logs:")
    for i in range(len(log_list)):
        parts = log_list[i][0].split("_")
        print("{0}: On track {1} at {2}:{3}:{4}".format(i, parts[0], parts[1][:2], parts[1][2:4], parts[1][4:]))

    if len(log_list) > 1:
        print("You can set a default log file name using LogName/LN command line parameter!")
        selected_log = int(input("Select track index: "))
    else:
        selected_log = 0

    if selected_log < 0:
        selected_log = 0
    if selected_log >= len(log_list):
        selected_log = len(log_list) - 1

    return r"{0}\{1}{2}".format(folder_name, log_list[selected_log][0], log_list[selected_log][1])


def get_track_file(track_folder_path, log_file):
    with open(log_file, "r") as text_file:
        track_file_name = text_file.readline()
    return r"{0}\{1}".format(track_folder_path, track_file_name.strip())


def create_cars(log_file_name):
    car_list = []
    with open(log_file_name, "r") as text_file:
        text_file.readline()
        new_line = text_file.readline()
        while len(new_line.strip()) > 0:
            car_list.append(
                Car(
                    driver=DriverBase(""),
                    initial_position=track.get_start(),
                    color=color_source.get_next_color()
                )
            )
            car_list[-1].deserialize_positions(new_line)
            new_line = text_file.readline()

    return car_list


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Command line arguments: "
              "TF:<track descriptor YAML folder> LF:<folder of race results> VT:<visualization type: Animated/Still>")

    settings = Settings(sys.argv)

    track_folder = settings.get_parameter_by_key("TracksFolder", "Tracks")
    log_folder = settings.get_parameter_by_key("LogsFolder", "Logs")

    if settings.get_parameter_by_key("LogName", None) is None:
        log_descriptor = select_log(log_folder)
    else:
        log_descriptor = r"{0}\{1}".format(log_folder, settings.get_parameter_by_key("LogName")),

    visualization_type = settings.get_parameter_by_key("VisualizationType", "Animated")

    track = Track(get_track_file(track_folder, log_descriptor))

    color_source = ColorSource()

    cars = create_cars(log_descriptor)

    if visualization_type.lower() == "still":
        visualizer = ImageVisualizer(
            track=track,
            track_image=track.get_track(), down_sample=1,
            cars=cars, path_color_coefficient=0.6
        )
        visualizer.create_image()
        visualizer.show_image()

    if visualization_type.lower() in ["animated", "continuous"] or visualization_type.lower().startswith("repeat:"):

        if visualization_type.lower().startswith("repeat:"):
            repeat = int(visualization_type[7:].strip())
        elif visualization_type.lower() == "animated":
            repeat = 1
        else:
            repeat = 0

        visualizer = AnimationVisualizer(
            track=track,
            track_image=track.get_track(), down_sample=1,
            cars=cars, path_color_coefficient=0.6,
            track_log_length=3,
            repeat=repeat
        )
        visualizer.show_animation(100)

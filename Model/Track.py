import numpy as np
import yaml

from PIL import Image

from Model.LinearAlgebra import LinearAlgebra
from Model.TrackSplit import TrackSplit


class Track:
    def __init__(self, descriptor_file_name):
        with open(descriptor_file_name) as stream:
            settings = yaml.safe_load(stream)

        self._track_image = np.array(Image.open(settings["image_file"]))
        self._name = settings["name"]
        self._down_sample = int(settings["down_sample"])
        self._track = self._track_image[::self._down_sample, ::self._down_sample, :]

        self._start_line = LinearAlgebra.create_vector(settings["start"], down_sample=self._down_sample)
        self._start_direction = LinearAlgebra.create_point(settings["start"]["direction"], 1)

        self._split_lines = [TrackSplit({"start": settings["start"]}, down_sample=self._down_sample)]
        for s in settings["splits"]:
            self._split_lines.append(
                TrackSplit(s, down_sample=self._down_sample)
            )

        self._track[self._track < 125] = 0
        self._track[self._track >= 125] = 255

    def get_name(self):
        return self._name

    def get_track(self):
        return self._track.copy()

    def get_track_image(self):
        return self._track_image.copy()

    def get_size(self):
        return self._track.shape[0], self._track.shape[1]

    def get_start(self):
        return LinearAlgebra.create_vector_halfway(self._start_line)

    def get_start_line(self):
        return self._start_line

    def get_split_lines(self):
        return self._split_lines

    def get_split_count(self):
        return len(self._split_lines)

    def get_split(self, index):
        return self._split_lines[index]

    def get_start_direction(self):
        return self._start_direction

    def is_point_on_map(self, coord):
        if 0 <= coord[0] < self._track.shape[0] and 0 <= coord[1] < self._track.shape[1]:
            return True
        else:
            return False

    def get_point(self, coord):
        if self.is_point_on_map(coord):
            return min(
                self._track[coord[0], coord[1], 0],
                self._track[coord[0], coord[1], 1],
                self._track[coord[0], coord[1], 2]
            )
        else:
            return 256

    def check_path(self, path):
        last_same_point = path[0]
        start_point_type = self.get_point(path[0])
        for c in path:
            if not self.is_point_on_map(c) or self.get_point(c) != start_point_type:
                return last_same_point
            else:
                last_same_point = c

        return last_same_point

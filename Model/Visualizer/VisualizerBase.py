from Model.Track import Track


class VisualizerBase:
    def __init__(self,
                 track: Track,
                 track_image, down_sample,
                 cars,
                 path_color_coefficient=0.6):
        self._track = track
        self._original_track_image = track_image
        self._track_image = track_image.copy()
        self._down_sample = down_sample
        self._cars = cars
        self._path_color_coefficient = path_color_coefficient

    def _draw_checkpoints(self):
        for s in self._track.get_split_lines():
            self._line(
                s.vector[0][0], s.vector[0][1],
                s.vector[1][0], s.vector[1][1],
                [0, 0, 255]
            )

        self._line(
            self._track.get_start_line()[0][0], self._track.get_start_line()[0][1],
            self._track.get_start_line()[1][0], self._track.get_start_line()[1][1],
            [0, 255, 0]
        )

    def _line(self, r0: int, c0: int, r1: int, c1: int, color=None):
        steps = max(abs(r1 - r0), abs(c1 - c0))
        if steps > 0:
            col_step = (c1 - c0) / steps
            row_step = (r1 - r0) / steps

            r = r0 + 0.5
            c = c0 + 0.5

            for s in range(steps + 1):
                if color is None:
                    pixel_color = self._original_track_image[int(r), int(c)]
                else:
                    pixel_color = color

                self._track_image[int(r), int(c)] = pixel_color

                r += row_step
                c += col_step

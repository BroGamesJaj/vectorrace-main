import matplotlib.patches as mpl_patches
import matplotlib.pyplot as plt

from matplotlib import animation

from Model.Visualizer.VisualizerBase import VisualizerBase


class AnimationVisualizer(VisualizerBase):
    def __init__(self, track, track_image, down_sample, cars, path_color_coefficient,
                 track_log_length: int, repeat: int = 1):
        super().__init__(track, track_image, down_sample, cars, path_color_coefficient)
        self._track_log_length = track_log_length
        self._figure = None
        self._image = None
        self._animation = None
        self._frame_count = 0
        self._repeat = repeat

    def show_animation(self, delay=500):
        self._figure = plt.figure(figsize=(13, 10))
        self._image = plt.imshow(self._track_image)

        if len(self._cars) == 0:
            print("No coordinate logs specified!")
            return

        self._frame_count = max(self._cars, key=lambda c: c.get_position_count()).get_position_count()

        self._animation = animation.FuncAnimation(
            self._figure,
            self._update_animation,
            frames=self._frame_count * (1 if self._repeat == 0 else self._repeat),
            interval=delay, repeat=self._repeat == 0
        )
        plt.title("Frame: ")

        colors = [[cc / 255.0 for cc in c.color] for c in self._cars]
        patches = [
            mpl_patches.Patch(color=colors[i], label="{0}".format(self._cars[i].get_driver_name()))
            for i in range(len(self._cars))
        ]
        plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        plt.show()

    def _update_animation(self, frame):
        frame = frame % self._frame_count
        if frame == 1:
            self._track_image = self._original_track_image.copy()

        path_color_time_coefficient = self._path_color_coefficient / self._track_log_length

        self._draw_checkpoints()

        for ci in range(len(self._cars)):
            dark_color = [int(cc * self._path_color_coefficient) for cc in self._cars[ci].color]

            if self._cars[ci].get_position(frame) is not None and frame > 0:
                self._line(
                    self._cars[ci].get_position(frame - 1)[0], self._cars[ci].get_position(frame - 1)[1],
                    self._cars[ci].get_position(frame)[0], self._cars[ci].get_position(frame)[1],
                    dark_color
                )

                for t in range(min(self._track_log_length, frame - 1)):
                    segment_color = [
                        int(dc * ((self._track_log_length - t) * path_color_time_coefficient)) for dc in dark_color
                    ]

                    segment_color = [sc if sc >= 0 else 0 for sc in segment_color]

                    self._line(
                        self._cars[ci].get_position(frame - t - 2)[0],
                        self._cars[ci].get_position(frame - t - 2)[1],
                        self._cars[ci].get_position(frame - t - 1)[0],
                        self._cars[ci].get_position(frame - t - 1)[1],
                        segment_color
                    )

        for ci in range(len(self._cars)):
            pos = self._cars[ci].get_position(frame, True)
            if pos is not None:
                self._track_image[pos[0], pos[1]] = self._cars[ci].color

        frame += 1

        if frame < self._frame_count:
            plt.title("Iteration: {0}/{1}".format(frame, self._frame_count))
        else:
            plt.title("Finished")

        self._image.set_data(self._track_image)
        self._figure.canvas.draw()

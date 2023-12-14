import matplotlib.patches as mpl_patches
import matplotlib.pyplot as plt

from Model.Visualizer.VisualizerBase import VisualizerBase


class ImageVisualizer(VisualizerBase):
    def create_image(self):
        self._track_image = self._track_image.copy()
        max_car_log_length = max(self._cars, key=lambda c: c.get_position_count()).get_position_count()

        if max_car_log_length == 1:
            for ci in range(len(self._cars)):
                if self._cars[ci].get_position_count() > 0:
                    self._track_image[
                        self._cars[ci].get_position(0)[0], self._cars[ci].get_position(0)[1]
                    ] = self._cars[ci].color
        else:
            for pi in range(1, max_car_log_length):
                for ci in range(len(self._cars)):
                    dark_color = [int(cc * self._path_color_coefficient) for cc in self._cars[ci].color]

                    if self._cars[ci].get_position(pi) is not None:
                        self._line(
                            self._cars[ci].get_position(pi - 1)[0], self._cars[ci].get_position(pi - 1)[1],
                            self._cars[ci].get_position(pi)[0], self._cars[ci].get_position(pi)[1],
                            dark_color
                        )

                        self._track_image[
                            self._cars[ci].get_position(pi - 1)[0], self._cars[ci].get_position(pi - 1)[1]
                        ] = self._cars[ci].color

                        self._track_image[
                            self._cars[ci].get_position(pi)[0], self._cars[ci].get_position(pi)[1]
                        ] = self._cars[ci].color

        self._draw_checkpoints()

    def get_image(self):
        return self._track_image

    def show_image(self):
        plt.figure(figsize=(13, 10))
        plt.imshow(self._track_image)
        colors = [[cc / 255.0 for cc in c.color] for c in self._cars]
        patches = [mpl_patches.Patch(color=colors[i], label="{0}".format(self._cars[i].get_driver_name())) for i in
                   range(len(self._cars))]
        plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()

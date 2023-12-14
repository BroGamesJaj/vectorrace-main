import matplotlib.pyplot as plt


class ColorSource:
    def __init__(self):
        self._colors = [(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)) for c in plt.get_cmap("Set3").colors]
        self._current_color_index = 0

    def get_next_color(self):
        color = self._colors[self._current_color_index]

        self._current_color_index += 1
        if self._current_color_index >= len(self._colors):
            self._current_color_index = 0

        return color

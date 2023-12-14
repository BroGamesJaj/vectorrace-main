from Model.Sensors.PathSensorBase import PathSensorBase


class LineSensor(PathSensorBase):
    def is_path_homogeneous(self, start_coordinates, end_coordinates):
        return super().is_path_homogeneous(start_coordinates, end_coordinates)

    def _get_path(self, r0, c0, r1, c1):
        coords = list()

        steps = max(abs(r1 - r0), abs(c1 - c0))
        if steps == 0:
            coords = [(r0, c0), (r1, c1)]
        else:
            col_step = (c1 - c0) / steps
            row_step = (r1 - r0) / steps

            y = r0 + 0.5
            x = c0 + 0.5
            for s in range(steps + 1):
                coords.append(
                    (int(y), int(x))
                )
                y += row_step
                x += col_step

        return coords

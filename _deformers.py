import math

from PIL import Image


class WaveDeformer:
    def __init__(self, gridspace=20, sin_period_factor=40, x_dir=True, y_dir=True):
        self.gridspace = gridspace
        self.sin_amp = gridspace / 2
        self.sin_period_factor = sin_period_factor
        self.x_dir = x_dir
        self.y_dir = y_dir

    def transform_y(self, x, y):
        y = y + self.sin_amp * math.sin(x / self.sin_period_factor)
        return x, y

    def transform_x(self, x, y):
        x = x + self.sin_amp * math.sin(y / self.sin_period_factor)
        return x, y

    def transform_xy(self, x, y) -> tuple[int, int]:
        x2 = x + self.sin_amp * math.sin(y / self.sin_period_factor)
        y2 = y + self.sin_amp * math.sin(x / self.sin_period_factor)
        return x2, y2

    def transform_rectangle(
        self, x0, y0, x1, y1
    ) -> tuple[int, int, int, int, int, int, int, int]:
        if self.x_dir and self.y_dir:
            return (
                *self.transform_xy(x0, y0),
                *self.transform_xy(x0, y1),
                *self.transform_xy(x1, y1),
                *self.transform_xy(x1, y0),
            )
        elif self.x_dir:
            return (
                *self.transform_x(x0, y0),
                *self.transform_x(x0, y1),
                *self.transform_x(x1, y1),
                *self.transform_x(x1, y0),
            )
        elif self.y_dir:
            return (
                *self.transform_y(x0, y0),
                *self.transform_y(x0, y1),
                *self.transform_y(x1, y1),
                *self.transform_y(x1, y0),
            )
        else:
            return (
                *self.transform_xy(x0, y0),
                *self.transform_xy(x0, y1),
                *self.transform_xy(x1, y1),
                *self.transform_xy(x1, y0),
            )

    def getmesh(
        self, image: Image.Image
    ) -> list[
        tuple[tuple[int, int, int, int], tuple[int, int, int, int, int, int, int, int]]
    ]:
        self.w, self.h = image.size
        self.gridspace

        target_grid = []

        for x in range(0, self.w, self.gridspace):
            for y in range(0, self.h, self.gridspace):
                target_grid.append((x, y, x + self.gridspace, y + self.gridspace))
        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]

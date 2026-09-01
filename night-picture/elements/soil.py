from elements.element import Element
from palette import SOIL_BOTTOM, SOIL_RIM, SOIL_TOP


class Soil(Element):
    def __init__(self, terrain, right_x, samples=90):
        self.terrain = terrain
        self.right_x = right_x
        self.samples = samples

    def _surface_points(self):
        points = []
        start = self.terrain.edge_x
        for index in range(self.samples + 1):
            x = start + (self.right_x - start) * index / self.samples
            points.append((x, self.terrain.height_at(x)))
        return points

    def render(self, painter, time):
        surface = self._surface_points()

        painter.alpha_blend()
        body = []
        for x, top in surface:
            body.append((x, 0.0, top, SOIL_BOTTOM, SOIL_TOP))
        painter.column_strip(body)

        painter.additive_blend()
        rim_rgb = SOIL_RIM[:3]
        rim = []
        for x, top in surface:
            rim.append(
                (
                    x,
                    top - 2.0,
                    top + 3.0,
                    (rim_rgb[0], rim_rgb[1], rim_rgb[2], 0.0),
                    (rim_rgb[0], rim_rgb[1], rim_rgb[2], 0.22),
                )
            )
        painter.column_strip(rim)

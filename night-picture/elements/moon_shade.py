import math

from elements.element import Element
from palette import REFLECTION


class MoonShade(Element):
    def __init__(self, moon_x, waterline, size, rows=64):
        self.moon_x = moon_x
        self.waterline = waterline
        self.size = size
        self.rows = rows

    def render(self, painter, time):
        painter.additive_blend()
        reflection_rgb = REFLECTION[:3]
        for row in range(self.rows):
            depth = row / self.rows
            next_depth = (row + 1) / self.rows
            y_top = self.waterline * (1.0 - depth)
            y_bottom = self.waterline * (1.0 - next_depth)
            shimmer = 0.55 + 0.45 * abs(math.sin(depth * 26.0 - time * 2.2))
            falloff = math.exp(-depth * 2.4)
            alpha = 0.42 * falloff * shimmer
            half_width = self.size * 0.5 * (0.35 + depth * 1.5)
            sway = 10.0 * math.sin(depth * 7.0 + time * 1.3)
            center_x = self.moon_x + sway
            center_color = (reflection_rgb[0], reflection_rgb[1], reflection_rgb[2], alpha)
            edge_color = (reflection_rgb[0], reflection_rgb[1], reflection_rgb[2], 0.0)
            painter.horizontal_beam(center_x, y_bottom, y_top, half_width, center_color, edge_color)

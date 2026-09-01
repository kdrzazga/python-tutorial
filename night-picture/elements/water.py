import math

from elements.element import Element
from palette import RIPPLE, WATER_BOTTOM, WATER_TOP


class Water(Element):
    def __init__(self, width, waterline, rng, ripple_count=7):
        self.width = width
        self.waterline = waterline
        self.ripples = tuple(self._scatter_ripples(rng, ripple_count))

    def _scatter_ripples(self, rng, count):
        ripples = []
        for _ in range(count):
            height = rng.uniform(self.waterline * 0.08, self.waterline * 0.92)
            phase = rng.uniform(0.0, 2.0 * math.pi)
            speed = rng.uniform(0.4, 1.1)
            strength = rng.uniform(0.04, 0.12)
            ripples.append((height, phase, speed, strength))
        return ripples

    def render(self, painter, time):
        painter.alpha_blend()
        painter.gradient_rect(0.0, 0.0, self.width, self.waterline, WATER_BOTTOM, WATER_TOP)

        painter.additive_blend()
        ripple_rgb = RIPPLE[:3]
        for height, phase, speed, strength in self.ripples:
            band = strength * (0.6 + 0.4 * math.sin(time * speed + phase))
            painter.horizontal_beam(
                self.width * 0.5,
                height - 1.0,
                height + 1.0,
                self.width * 0.5,
                (ripple_rgb[0], ripple_rgb[1], ripple_rgb[2], band),
                (ripple_rgb[0], ripple_rgb[1], ripple_rgb[2], 0.0),
            )

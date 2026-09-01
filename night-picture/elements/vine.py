import math

from elements.element import Element
from palette import VINE


class LightStrand:
    def __init__(self, x, y_top, length, sway_amplitude, sway_frequency, phase, dot_gap, drift_speed):
        self.x = x
        self.y_top = y_top
        self.length = length
        self.sway_amplitude = sway_amplitude
        self.sway_frequency = sway_frequency
        self.phase = phase
        self.dot_gap = dot_gap
        self.drift_speed = drift_speed

    def render(self, painter, time):
        dot_count = max(int(self.length / self.dot_gap), 1)
        rgb = VINE[:3]
        for index in range(dot_count + 1):
            fraction = index / dot_count
            y = self.y_top - fraction * self.length
            sway = self.sway_amplitude * fraction
            x = self.x + sway * math.sin(self.sway_frequency * fraction * math.pi + time * self.drift_speed + self.phase)
            alpha = (1.0 - fraction * 0.85) * (0.55 + 0.45 * math.sin(time * 2.0 + self.phase + fraction * 6.0))
            size = 2.6 * (1.0 - fraction * 0.4)
            painter.glow_dot(x, y, size, (rgb[0], rgb[1], rgb[2], max(alpha, 0.0)), 8)


class Vines(Element):
    def __init__(self, anchor_x, anchor_y, spread, count, rng):
        self.strands = tuple(self._grow(anchor_x, anchor_y, spread, count, rng))

    def _grow(self, anchor_x, anchor_y, spread, count, rng):
        strands = []
        for _ in range(count):
            x = anchor_x + rng.uniform(-spread, spread)
            y_top = anchor_y + rng.uniform(-spread * 0.3, spread * 0.3)
            length = rng.uniform(70.0, 210.0)
            sway_amplitude = rng.uniform(6.0, 18.0)
            sway_frequency = rng.uniform(1.0, 2.4)
            phase = rng.uniform(0.0, 2.0 * math.pi)
            dot_gap = rng.uniform(9.0, 15.0)
            drift_speed = rng.uniform(0.6, 1.4)
            strands.append(
                LightStrand(x, y_top, length, sway_amplitude, sway_frequency, phase, dot_gap, drift_speed)
            )
        return strands

    def render(self, painter, time):
        painter.additive_blend()
        for strand in self.strands:
            strand.render(painter, time)

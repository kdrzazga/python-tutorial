import math

from elements.element import Element
from palette import FIREFLY


class Firefly:
    def __init__(self, center_x, center_y, amplitude_x, amplitude_y, speed_x, speed_y, phase_x, phase_y, size, blink_phase):
        self.center_x = center_x
        self.center_y = center_y
        self.amplitude_x = amplitude_x
        self.amplitude_y = amplitude_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.phase_x = phase_x
        self.phase_y = phase_y
        self.size = size
        self.blink_phase = blink_phase

    def render(self, painter, time):
        x = self.center_x + self.amplitude_x * math.sin(self.speed_x * time + self.phase_x)
        y = self.center_y + self.amplitude_y * math.sin(self.speed_y * time + self.phase_y)
        brightness = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(time * 2.0 + self.blink_phase))
        rgb = FIREFLY[:3]
        painter.glow_dot(x, y, self.size, (rgb[0], rgb[1], rgb[2], brightness), 10)


class Swarm(Element):
    def __init__(self, region_x, region_y, region_width, region_height, count, rng):
        self.fireflies = tuple(
            self._scatter(region_x, region_y, region_width, region_height, count, rng)
        )

    def _scatter(self, region_x, region_y, region_width, region_height, count, rng):
        fireflies = []
        for _ in range(count):
            center_x = region_x + rng.uniform(0.0, region_width)
            center_y = region_y + rng.uniform(0.0, region_height)
            amplitude_x = rng.uniform(8.0, 34.0)
            amplitude_y = rng.uniform(8.0, 30.0)
            speed_x = rng.uniform(0.3, 0.9)
            speed_y = rng.uniform(0.3, 0.9)
            phase_x = rng.uniform(0.0, 2.0 * math.pi)
            phase_y = rng.uniform(0.0, 2.0 * math.pi)
            size = rng.uniform(2.0, 4.5)
            blink_phase = rng.uniform(0.0, 2.0 * math.pi)
            fireflies.append(
                Firefly(center_x, center_y, amplitude_x, amplitude_y, speed_x, speed_y, phase_x, phase_y, size, blink_phase)
            )
        return fireflies

    def render(self, painter, time):
        painter.additive_blend()
        for firefly in self.fireflies:
            firefly.render(painter, time)

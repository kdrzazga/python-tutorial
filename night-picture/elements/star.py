import math

from elements.element import Element
from palette import STAR


class Star:
    def __init__(self, x, y, brightness, size, phase, twinkle_speed):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.size = size
        self.phase = phase
        self.twinkle_speed = twinkle_speed

    def render(self, painter, time):
        flicker = 0.6 + 0.4 * math.sin(time * self.twinkle_speed + self.phase)
        alpha = self.brightness * flicker
        painter.glow_dot(self.x, self.y, self.size, (STAR[0], STAR[1], STAR[2], alpha), 10)


class StarField(Element):
    def __init__(self, width, height, count, rng, avoid_x, avoid_y, avoid_radius, horizon):
        self.stars = tuple(
            self._scatter(width, height, count, rng, avoid_x, avoid_y, avoid_radius, horizon)
        )

    def _scatter(self, width, height, count, rng, avoid_x, avoid_y, avoid_radius, horizon):
        stars = []
        attempts = 0
        while len(stars) < count and attempts < count * 12:
            attempts += 1
            x = rng.uniform(0.0, width)
            y = rng.uniform(horizon, height)
            if math.hypot(x - avoid_x, y - avoid_y) < avoid_radius:
                continue
            brightness = rng.uniform(0.25, 0.95)
            size = rng.uniform(1.2, 3.0)
            phase = rng.uniform(0.0, 2.0 * math.pi)
            twinkle_speed = rng.uniform(0.8, 2.6)
            stars.append(Star(x, y, brightness, size, phase, twinkle_speed))
        return stars

    def render(self, painter, time):
        painter.additive_blend()
        for star in self.stars:
            star.render(painter, time)

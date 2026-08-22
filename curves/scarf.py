import math

import pygame


class Scarf:
    def __init__(self, width=800, height=800, scale=280, speed=0.01):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (width // 2, height // 2)
        self.title = "Scarf"
        self.formula = "y = 0.3·sin(3x) ± 0.12,   |x| ≤ 1"

        self.amp = 0.3
        self.freq = 3
        self.half = 0.12
        self.outline = self.build_outline()

    def wave(self, x):
        return self.amp * math.sin(self.freq * x)

    def build_outline(self):
        points = []
        xs = [-1.0 + 2.0 * i / 120 for i in range(121)]
        for x in xs:
            points.append((x, self.wave(x) + self.half))
        for x in reversed(xs):
            points.append((x, self.wave(x) - self.half))
        points.append(points[0])
        return points

    def to_screen(self, point):
        x, y = point
        sx = self.center[0] + self.scale * x
        sy = self.center[1] - self.scale * y
        return sx, sy

    def build_points(self):
        count = int(self.progress * len(self.outline))
        return self.outline[:count]

    def draw(self, surface):
        surface.fill((10, 10, 20))
        points = self.build_points()
        for i in range(len(points) - 1):
            pygame.draw.line(surface, (200, 40, 50),
                             self.to_screen(points[i]),
                             self.to_screen(points[i + 1]), 3)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

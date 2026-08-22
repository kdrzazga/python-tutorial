import math

import pygame

RED = (200, 40, 50)
WHITE = (240, 240, 245)


class WinterCap:
    def __init__(self, width=800, height=800, scale=320, speed=0.012):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (int(width * 0.6), height // 2)
        self.title = "WinterCap"
        self.formula = [
            "dome:  x² + y² = 0.5²,  y ≥ 0",
            "brim:  |x| ≤ 0.55,  −0.15 ≤ y ≤ 0.02",
            "pom:   x² + (y − 0.55)² = 0.12²",
        ]

        self.parts = [
            ("poly", self.dome(0.5), RED),
            ("rect", (-0.55, -0.15, 0.55, 0.02), WHITE),
            ("circle", (0.0, 0.55, 0.12), WHITE),
        ]

    def dome(self, r):
        points = []
        steps = 80
        for i in range(steps + 1):
            angle = math.pi * i / steps
            points.append((r * math.cos(angle), r * math.sin(angle)))
        return points

    def to_screen(self, point):
        x, y = point
        return self.center[0] + self.scale * x, self.center[1] - self.scale * y

    def draw_part(self, surface, part):
        kind = part[0]
        if kind == "circle":
            cx, cy, r = part[1]
            pygame.draw.circle(surface, part[2], self.to_screen((cx, cy)),
                               max(2, int(self.scale * r)))
        elif kind == "rect":
            x0, y0, x1, y1 = part[1]
            corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
            pygame.draw.polygon(surface, part[2], [self.to_screen(p) for p in corners])
        elif kind == "poly":
            pygame.draw.polygon(surface, part[2], [self.to_screen(p) for p in part[1]])

    def draw(self, surface):
        surface.fill((10, 10, 20))
        count = min(len(self.parts), int(self.progress * len(self.parts)) + 1)
        for part in self.parts[:count]:
            self.draw_part(surface, part)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

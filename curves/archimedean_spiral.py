import math

import pygame


class ArchimedeanSpiral:
    def __init__(self, width=800, height=800, scale=15, speed=0.01, turns=6):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.turns = turns
        self.progress = 0.0
        self.center = (width // 2, height // 2)
        self.title = "ArchimedeanSpiral"
        self.formula = "r(θ) = θ / 2"

    def polar_point(self, theta):
        r = theta / 2
        x = self.center[0] + self.scale * r * math.cos(theta)
        y = self.center[1] + self.scale * r * math.sin(theta)
        return x, y

    def build_points(self):
        points = []
        max_theta = self.progress * self.turns * 2 * math.pi
        steps = int(self.progress * 2000) + 1
        for i in range(steps + 1):
            theta = max_theta * i / steps
            points.append(self.polar_point(theta))
        return points

    def draw(self, surface):
        surface.fill((10, 10, 20))
        points = self.build_points()
        count = len(points)
        for i in range(count - 1):
            t = i / max(count - 1, 1)
            color = (
                int(100 + 155 * t),
                int(200 - 100 * t),
                int(150 + 105 * (1 - t)),
            )
            pygame.draw.line(surface, color, points[i], points[i + 1], 2)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

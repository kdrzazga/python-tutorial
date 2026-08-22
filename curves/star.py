import math

import pygame


class Star:
    def __init__(self, width=800, height=800, scale=140, speed=0.01,
                 points=5, inner_ratio=0.42, color=(255, 215, 0)):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.points = points
        self.inner_ratio = inner_ratio
        self.color = color
        self.progress = 0.0
        self.center = (width // 2, height // 2)
        self.title = "Star"
        self.formula = "r(θ) = r_in + (r_out − r_in)·|s/(π/n) − 1|,  s = θ mod (2π/n)"

    def radius(self, theta):
        sector = math.pi / self.points
        s = theta % (2 * sector)
        wave = abs(s / sector - 1)
        return self.inner_ratio + (1 - self.inner_ratio) * wave

    def polar_point(self, theta):
        r = self.radius(theta - math.pi / 2)
        x = self.center[0] + self.scale * r * math.cos(theta)
        y = self.center[1] - self.scale * r * math.sin(theta)
        return x, y

    def build_points(self):
        points = []
        max_theta = self.progress * 2 * math.pi
        steps = int(self.progress * 2000) + 1
        for i in range(steps + 1):
            theta = max_theta * i / steps
            points.append(self.polar_point(theta))
        return points

    def outline(self, cx, cy, size):
        vertices = []
        for i in range(2 * self.points + 1):
            theta = -math.pi / 2 + i * math.pi / self.points
            r = self.radius(theta + math.pi / 2)
            vertices.append((cx + size * r * math.cos(theta),
                             cy + size * r * math.sin(theta)))
        return vertices

    def draw_at(self, surface, cx, cy, size):
        pygame.draw.polygon(surface, self.color, self.outline(cx, cy, size))

    def draw(self, surface):
        surface.fill((10, 10, 20))
        points = self.build_points()
        for i in range(len(points) - 1):
            pygame.draw.line(surface, self.color, points[i], points[i + 1], 2)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

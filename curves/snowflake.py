import math

import pygame


class Snowflake:
    def __init__(self, width=800, height=800, scale=190, speed=0.01):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (width // 2, height // 2)
        self.title = "Snowflake"
        self.formula = "r(θ) = 0.55 + 1.3·max(0, cos 6θ)³ + 0.35·max(0, −cos 6θ)³"

    def radius(self, theta):
        main = max(0.0, math.cos(6 * theta))
        side = max(0.0, -math.cos(6 * theta))
        return 0.55 + 1.3 * main ** 3 + 0.35 * side ** 3

    def polar_point(self, theta):
        r = self.radius(theta)
        x = self.center[0] + self.scale * r * math.cos(theta)
        y = self.center[1] + self.scale * r * math.sin(theta)
        return x, y

    def build_points(self):
        points = []
        max_theta = self.progress * 2 * math.pi
        steps = int(self.progress * 2000) + 1
        for i in range(steps + 1):
            theta = max_theta * i / steps
            points.append(self.polar_point(theta))
        return points

    def draw(self, surface):
        surface.fill((10, 10, 20))
        points = self.build_points()
        for i in range(len(points) - 1):
            pygame.draw.line(surface, (180, 220, 255), points[i], points[i + 1], 2)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0


class Snowflake2(Snowflake):
    def __init__(self, width=800, height=800, scale=170, speed=0.01):
        super().__init__(width, height, scale, speed)
        self.title = "Snowflake2"
        self.formula = ("r(θ) = 0.5 + 1.2·max(0, cos 6θ)³ + 0.3·max(0, −cos 6θ)³ "
                        "+ 0.15·max(0, cos 18θ)⁶·max(0, cos 6θ)")

    def radius(self, theta):
        main = max(0.0, math.cos(6 * theta))
        side = max(0.0, -math.cos(6 * theta))
        branches = max(0.0, math.cos(18 * theta))
        return 0.5 + 1.2 * main ** 3 + 0.3 * side ** 3 + 0.15 * branches ** 6 * main

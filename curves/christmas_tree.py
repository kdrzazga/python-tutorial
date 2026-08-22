import pygame

from star import Star


class ChristmasTree:
    def __init__(self, width=800, height=800, scale=230, speed=0.01):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (width // 2, height // 2 + 120 - int(height * 0.26))
        self.title = "ChristmasTree"
        self.formula = [
            "foliage:  w(y) = w_k·(0.35 + 0.65·f),   f within [0, 1]",
            "trunk:    |x| ≤ 0.1,   y ≤ −0.9",
            "star:     r(θ) = r_in + (r_out − r_in)·|s/(π/n) − 1|",
        ]

        self.top = 1.0
        self.bottom = -0.9
        self.tiers = 3
        self.base_width = 0.95
        self.trunk_width = 0.1
        self.trunk_height = 0.35

        self.star = Star()
        self.outline = self.build_outline()

    def half_width(self, y):
        span = self.top - self.bottom
        tier_span = span / self.tiers
        depth = self.top - y
        k = min(int(depth / tier_span), self.tiers - 1)
        local = (depth - k * tier_span) / tier_span
        tier_max = self.base_width * (k + 1) / self.tiers
        return tier_max * (0.35 + 0.65 * local)

    def build_outline(self):
        points = []
        steps = 160

        points.append((0.0, self.top))

        for i in range(1, steps + 1):
            y = self.top - (self.top - self.bottom) * i / steps
            points.append((-self.half_width(y), y))

        trunk_bottom = self.bottom - self.trunk_height
        points.append((-self.trunk_width, self.bottom))
        points.append((-self.trunk_width, trunk_bottom))
        points.append((self.trunk_width, trunk_bottom))
        points.append((self.trunk_width, self.bottom))

        for i in range(steps + 1):
            y = self.bottom + (self.top - self.bottom) * i / steps
            points.append((self.half_width(y), y))

        return points

    def to_screen(self, point):
        x, y = point
        sx = self.center[0] + self.scale * x
        sy = self.center[1] - self.scale * y
        return sx, sy

    def is_trunk(self, point):
        x, y = point
        return y <= self.bottom + 1e-6 and abs(x) <= self.trunk_width + 1e-6

    def build_points(self):
        count = int(self.progress * len(self.outline))
        return self.outline[:count]

    def draw_star(self, surface):
        cx, cy = self.to_screen((0.0, self.top))
        self.star.draw_at(surface, cx, cy, 26)

    def draw(self, surface):
        surface.fill((10, 10, 20))
        points = self.build_points()
        for i in range(len(points) - 1):
            a = points[i]
            b = points[i + 1]
            if self.is_trunk(a) and self.is_trunk(b):
                color = (120, 72, 40)
            else:
                color = (40, 180, 90)
            pygame.draw.line(surface, color, self.to_screen(a), self.to_screen(b), 3)

        if self.progress >= 0.99:
            self.draw_star(surface)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

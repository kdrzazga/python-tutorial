import math

import pygame


class Snowman:
    def __init__(self, width=800, height=800, scale=300, speed=0.01):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (int(width * 0.70), height // 2)
        self.title = "Snowman"
        self.formula = [
            "bottom:  x² + (y + 0.55)² = 0.45²",
            "middle:  x² + (y − 0.23)² = 0.33²",
            "head:    x² + (y − 0.78)² = 0.22²",
            "nose:    △ (0, 0.80), (0, 0.76), (0.20, 0.78)",
            "arms:    y = 0.30 + 0.56·(|x| − 0.30),  0.30 ≤ |x| ≤ 0.66",
            "eyes:    (|x| − 0.07)² + (y − 0.84)² = 0.028²",
            "buttons: x² + (y − b)² = 0.028²,  b ∈ {0.10, 0.23, 0.36}",
            "scarf:   y = 0.56 + 0.04·sin(14x),  |x| ≤ 0.24",
            "tail:    x = 0.20 + 0.03·sin(20y),  0.16 ≤ y ≤ 0.56",
        ]

        self.balls = [
            (0.0, -0.55, 0.45),
            (0.0, 0.23, 0.33),
            (0.0, 0.78, 0.22),
        ]
        self.ball_outlines = [self.build_circle(cx, cy, r) for cx, cy, r in self.balls]
        self.total = sum(len(outline) for outline in self.ball_outlines)

        self.eyes = [(-0.07, 0.84), (0.07, 0.84)]
        self.buttons = [(0.0, 0.36), (0.0, 0.23), (0.0, 0.10)]
        self.mouth = [(-0.09, 0.74), (-0.045, 0.72), (0.0, 0.715),
                      (0.045, 0.72), (0.09, 0.74)]
        self.nose = [(0.0, 0.80), (0.0, 0.76), (0.20, 0.78)]
        self.left_arm = [(-0.30, 0.30), (-0.66, 0.50)]
        self.right_arm = [(0.30, 0.30), (0.66, 0.50)]
        self.left_twig = [(-0.55, 0.44), (-0.60, 0.60)]
        self.right_twig = [(0.55, 0.44), (0.60, 0.60)]

        self.scarf = [(x, 0.56 + 0.04 * math.sin(14 * x))
                      for x in self.span(-0.24, 0.24, 60)]
        self.scarf_tail = [(0.20 + 0.03 * math.sin(20 * y), y)
                           for y in self.span(0.56, 0.16, 50)]

    def span(self, start, end, count):
        return [start + (end - start) * i / (count - 1) for i in range(count)]

    def build_circle(self, cx, cy, r):
        points = []
        steps = 160
        for i in range(steps + 1):
            phi = 2 * math.pi * i / steps
            points.append((cx + r * math.cos(phi), cy + r * math.sin(phi)))
        return points

    def to_screen(self, point):
        x, y = point
        sx = self.center[0] + self.scale * x
        sy = self.center[1] - self.scale * y
        return sx, sy

    def dot(self, surface, point, r_units, color):
        pygame.draw.circle(surface, color, self.to_screen(point),
                           max(2, int(self.scale * r_units)))

    def draw_details(self, surface):
        black = (20, 20, 20)
        brown = (120, 72, 40)
        red = (200, 40, 50)

        scarf_width = max(6, int(self.scale * 0.05))
        pygame.draw.lines(surface, red, False,
                          [self.to_screen(p) for p in self.scarf], scarf_width)
        pygame.draw.lines(surface, red, False,
                          [self.to_screen(p) for p in self.scarf_tail], scarf_width)

        pygame.draw.line(surface, brown, self.to_screen(self.left_arm[0]),
                         self.to_screen(self.left_arm[1]), 3)
        pygame.draw.line(surface, brown, self.to_screen(self.right_arm[0]),
                         self.to_screen(self.right_arm[1]), 3)
        pygame.draw.line(surface, brown, self.to_screen(self.left_twig[0]),
                         self.to_screen(self.left_twig[1]), 3)
        pygame.draw.line(surface, brown, self.to_screen(self.right_twig[0]),
                         self.to_screen(self.right_twig[1]), 3)

        pygame.draw.polygon(surface, (240, 140, 30),
                            [self.to_screen(p) for p in self.nose])

        for eye in self.eyes:
            self.dot(surface, eye, 0.028, black)
        for spot in self.mouth:
            self.dot(surface, spot, 0.018, black)
        for button in self.buttons:
            self.dot(surface, button, 0.028, black)

    def draw(self, surface):
        surface.fill((10, 10, 20))
        revealed = int(self.progress * self.total)
        drawn = 0
        for outline in self.ball_outlines:
            take = max(0, min(len(outline), revealed - drawn))
            for i in range(take - 1):
                pygame.draw.line(surface, (235, 235, 245),
                                 self.to_screen(outline[i]),
                                 self.to_screen(outline[i + 1]), 3)
            drawn += len(outline)

        if self.progress >= 0.99:
            self.draw_details(surface)

    def update(self):
        self.progress += self.speed

    def is_complete(self):
        return self.progress >= 1.0

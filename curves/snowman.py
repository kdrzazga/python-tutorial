import math

import pygame


class Snowman:
    def __init__(self, width=800, height=800, scale=240, speed=0.01):
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
            "arms:    y = 0.30 + 0.58·(|x| − 0.30),  0.30 ≤ |x| ≤ 0.85",
            "eyes:    (|x| − 0.07)² + (y − 0.84)² = 0.028²",
            "brows:   arcs above eyes near y ≈ 0.89",
            "hat:     brim |x| ≤ 0.30, body |x| ≤ 0.20, band red,  0.95 ≤ y ≤ 1.34",
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
        self.brows = [
            [(-0.11, 0.885), (-0.075, 0.905), (-0.04, 0.89)],
            [(0.04, 0.89), (0.075, 0.905), (0.11, 0.885)],
        ]
        self.mouth = [(-0.09, 0.74), (-0.045, 0.72), (0.0, 0.715),
                      (0.045, 0.72), (0.09, 0.74)]
        self.nose = [(0.0, 0.80), (0.0, 0.76), (0.15, 0.78)]

        self.hat_body = (-0.20, 1.02, 0.20, 1.34)
        self.hat_brim = (-0.30, 0.95, 0.30, 1.03)
        self.hat_band = (-0.20, 1.03, 0.20, 1.11)
        self.left_arm = [(-0.2958, 0.3667), (-0.7375, 0.595)]
        self.right_arm = [(0.2375, 0.3375), (0.7875, 0.6575)]
        self.left_twig = [(-0.6075, 0.505), (-0.6875, 0.705)]
        self.right_twig = [(0.6575, 0.5675), (0.7375, 0.7675)]

        self.scarf = [(x, 0.56 + 0.04 * math.sin(14 * x))
                      for x in self.span(-0.24, 0.24, 60)]
        self.scarf_tail = [(0.20 + 0.03 * math.sin(20 * y), y)
                           for y in self.span(0.56, 0.16, 50)]
        self.show_scarf = True
        self.show_balls = True
        self.fill_background = True

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

    def fill_rect(self, surface, box, color):
        x0, y0, x1, y1 = box
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        pygame.draw.polygon(surface, color, [self.to_screen(p) for p in corners])

    def draw_details(self, surface):
        black = (20, 20, 20)
        brown = (120, 72, 40)
        red = (200, 40, 50)
        hat_brown = (120, 95, 75)

        self.fill_rect(surface, self.hat_body, hat_brown)
        self.fill_rect(surface, self.hat_brim, hat_brown)
        self.fill_rect(surface, self.hat_band, red)

        if self.show_scarf:
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
        for brow in self.brows:
            pygame.draw.lines(surface, black, False,
                              [self.to_screen(p) for p in brow], 3)
        for spot in self.mouth:
            self.dot(surface, spot, 0.018, black)

    def draw(self, surface):
        if self.fill_background:
            surface.fill((10, 10, 20))
        if self.show_balls:
            revealed = int(self.progress * self.total)
            drawn = 0
            for outline in self.ball_outlines:
                take = max(0, min(len(outline), revealed - drawn))
                if take >= len(outline):
                    pygame.draw.polygon(surface, (235, 235, 245),
                                        [self.to_screen(p) for p in outline])
                else:
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

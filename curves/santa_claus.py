import pygame

RED = (200, 40, 50)
WHITE = (240, 240, 245)
SKIN = (255, 224, 189)
BLACK = (20, 20, 20)
NOSE = (230, 150, 140)


class SantaClaus:
    def __init__(self, width=800, height=800, scale=250, speed=0.012):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (int(width * 0.6), height // 2)
        self.title = "SantaClaus"
        self.formula = [
            "face:  x² + y² = 0.38²",
            "hat:   △ (−0.37, 0.14), (0.37, 0.14), (0.12, 0.88)",
            "brim:  |x| ≤ 0.40,  0.12 ≤ y ≤ 0.24",
            "beard: x² + (y + 0.34)² = 0.34²",
            "eyes:  (|x| − 0.13)² + (y − 0.10)² = 0.032²",
            "nose:  x² + (y − 0.03)² = 0.06²",
        ]

        self.parts = [
            ("circle", (0.0, 0.0, 0.38), SKIN),
            ("poly", [(-0.37, 0.14), (0.37, 0.14), (0.12, 0.88)], RED),
            ("rect", (-0.40, 0.12, 0.40, 0.24), WHITE),
            ("circle", (0.12, 0.90, 0.09), WHITE),
            ("circle", (0.0, -0.34, 0.34), WHITE),
            ("circle", (-0.10, -0.02, 0.10), WHITE),
            ("circle", (0.10, -0.02, 0.10), WHITE),
            ("circle", (-0.13, 0.10, 0.032), BLACK),
            ("circle", (0.13, 0.10, 0.032), BLACK),
            ("circle", (0.0, 0.03, 0.06), NOSE),
        ]

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

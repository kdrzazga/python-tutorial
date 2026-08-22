import pygame

RED = (200, 40, 50)
WHITE = (240, 240, 245)


class Mittens:
    def __init__(self, width=800, height=800, scale=260, speed=0.012):
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.progress = 0.0
        self.center = (int(width * 0.6), height // 2)
        self.title = "Mittens"
        self.formula = [
            "palm:  (|x| − 0.5)² + (y − 0.12)² = 0.22²",
            "thumb: (|x| − 0.70)² + (y − 0.02)² = 0.10²",
            "cuff:  0.32 ≤ |x| ≤ 0.68,  −0.30 ≤ y ≤ −0.06",
        ]

        self.parts = self.build_mitten(-0.5, -1) + self.build_mitten(0.5, 1)

    def build_mitten(self, mx, thumb_dir):
        return [
            ("rect", (mx - 0.18, -0.30, mx + 0.18, -0.06), WHITE),
            ("rect", (mx - 0.18, -0.06, mx + 0.18, 0.12), RED),
            ("circle", (mx, 0.12, 0.22), RED),
            ("circle", (mx + thumb_dir * 0.20, 0.02, 0.10), RED),
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

import math

import pygame

from .face import Face
from .libs.colors import OSC_DARK_GREEN


class OscilloscopeFace(Face):
    def __init__(self, size):
        super().__init__(size, (5, 10, 5))
        self.history = []

    def render(self, t):
        surf = super().render(t)
        cx = cy = self.size / 2
        points = []
        for i in range(400):
            a = i / 400 * 2 * math.pi
            x = cx + math.sin(a * 3 + t * 1.5) * (self.size * 0.35)
            y = cy + math.sin(a * 2 + t * 2.1) * (self.size * 0.35)
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.lines(surf, OSC_DARK_GREEN, False, points, 2)
        pygame.draw.circle(surf, (30, 90, 40), (int(cx), int(cy)), int(self.size * 0.45), 1)
        pygame.draw.rect(surf, OSC_DARK_GREEN, (0, 0, self.size, self.size), 1)
        return surf

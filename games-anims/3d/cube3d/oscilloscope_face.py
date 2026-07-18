import math

import pygame

from .face import Face


class OscilloscopeFace(Face):
    """Scrolling Lissajous / waveform scope, like an old analog scope."""

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
            pygame.draw.lines(surf, (60, 255, 90), False, points, 2)
        pygame.draw.circle(surf, (30, 90, 40), (int(cx), int(cy)), int(self.size * 0.45), 1)
        return surf

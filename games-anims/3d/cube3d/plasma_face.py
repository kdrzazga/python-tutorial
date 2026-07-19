import numpy as np
import pygame

from libs.colors import hsv_to_rgb_array
from .face import Face


class PlasmaFace(Face):
    def __init__(self, size):
        super().__init__(size, (0, 0, 0))
        y, x = np.mgrid[0:size, 0:size].astype(np.float32)
        self.x = x / size
        self.y = y / size

    def render(self, t):
        x, y = self.x, self.y
        v = (
            np.sin((x * 10) + t)
            + np.sin((y * 10) + t * 1.3)
            + np.sin((x * 10 + y * 10) + t * 0.7)
            + np.sin(np.sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2) * 20 - t * 2)
        )
        hue = (v * 40 + t * 20) % 360
        hsv = np.stack([hue / 360.0, np.ones_like(hue), np.ones_like(hue)], axis=-1)
        rgb = hsv_to_rgb_array(hsv)
        arr = (rgb * 255).astype(np.uint8)
        surf = pygame.image.frombuffer(arr.tobytes(), (self.size, self.size), "RGB")
        return surf.convert()

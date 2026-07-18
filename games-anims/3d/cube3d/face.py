import pygame


class Face:
    """Base class for a live cube-face texture generator. Subclasses set
    `bg_color` and override `render` to draw on top of the filled surface
    this class produces."""

    def __init__(self, size, bg_color):
        self.size = size
        self.bg_color = bg_color

    def render(self, t):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.bg_color)
        return surf

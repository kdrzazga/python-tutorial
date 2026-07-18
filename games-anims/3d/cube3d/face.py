import pygame


class Face:
    def __init__(self, size, bg_color):
        self.size = size
        self.bg_color = bg_color

    def render(self, t):
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.bg_color)
        return surf

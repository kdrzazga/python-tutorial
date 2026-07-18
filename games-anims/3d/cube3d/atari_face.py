import pygame

from .colors import ATARI_BLUE, ATARI_CYAN
from .face import Face


class AtariFace(Face):
    def __init__(self, size):
        super().__init__(size, ATARI_BLUE)
        self.margin = int(size * 0.08)
        font_size = 8#max(5, size // 10)
        self.font = pygame.font.SysFont("couriernew,consolas,monospace", font_size, bold=True)
        self.line_height = self.font.get_linesize()
        self.cursor_w = self.font.size("@")[0]
        self.ready_surf = self.font.render("READY", True, ATARI_CYAN)

    def render(self, t):
        surf = super().render(t)

        x, y = self.margin, self.margin
        surf.blit(self.ready_surf, (x, y))

        cursor_y = y + self.line_height
        if int(t * 2) % 2 == 0:
            pygame.draw.rect(surf, ATARI_CYAN, (x, cursor_y, self.cursor_w, self.line_height - 2))

        return surf

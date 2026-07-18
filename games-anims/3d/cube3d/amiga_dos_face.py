import math

import pygame

from .colors import (
    AMIGA_BG,
    AMIGA_BLACK,
    AMIGA_CURSOR,
    AMIGA_POINTER,
    AMIGA_POINTER_DARK,
    AMIGA_WHITE,
)
from .face import Face
from .font_utils import fit_sysfont_size


class AmigaDOSFace(Face):
    LINES = [
        "Copyright ©1987 Commodore-Amiga, Inc.",
        "All rights reserved.",
        "Release 1.3",
    ]

    ARROW_POINTS = [
        (0, 0), (0, 16), (4, 12), (7, 18), (9, 17), (6, 11), (11, 11),
    ]

    def __init__(self, size):
        super().__init__(size, AMIGA_BG)
        self.scale = size / 256.0

        margin = int(size * 0.05)
        self.win_rect = pygame.Rect(margin, margin, size - 2 * margin, size - 2 * margin)
        self.title_h = max(12, int(size * 0.09))
        self.pad = int(size * 0.02)

        content_width = self.win_rect.width - 2 * self.pad
        font_size = fit_sysfont_size("couriernew,consolas,monospace", self.LINES + ["1>"],
                                      content_width, start_size=size // 10)
        self.font = pygame.font.SysFont("couriernew,consolas,monospace", font_size, bold=True)
        self.line_height = self.font.get_linesize()
        self.cursor_w = self.font.size("@")[0]
        self.prompt_surf = self.font.render("1>", True, AMIGA_WHITE)

        title_font_size = max(10, int(self.title_h * 0.55))
        self.title_font = pygame.font.SysFont("couriernew,consolas,monospace", title_font_size, bold=True)

    def render(self, t):
        surf = super().render(t)

        win = self.win_rect
        pygame.draw.rect(surf, AMIGA_WHITE, win, width=2)

        title_rect = pygame.Rect(win.left, win.top, win.width, self.title_h)
        pygame.draw.rect(surf, AMIGA_BLACK, title_rect)
        pygame.draw.rect(surf, AMIGA_WHITE, title_rect, width=2)

        gadget_size = self.title_h - 8
        gadget2 = pygame.Rect(title_rect.right - gadget_size - 4, title_rect.top + 4,
                               gadget_size, gadget_size)
        gadget1 = pygame.Rect(gadget2.left - gadget_size - 3, title_rect.top + 4,
                               gadget_size, gadget_size)
        pygame.draw.rect(surf, AMIGA_BLACK, gadget1)
        pygame.draw.rect(surf, AMIGA_WHITE, gadget1, 1)
        pygame.draw.rect(surf, AMIGA_WHITE, gadget2, 1)

        title_surf = self.title_font.render("AmigaDOS", True, AMIGA_WHITE)
        surf.blit(title_surf, (title_rect.left + 6, title_rect.centery - title_surf.get_height() // 2))

        x = win.left + self.pad
        y = title_rect.bottom + self.pad
        for line in self.LINES:
            line_surf = self.font.render(line, True, AMIGA_WHITE)
            surf.blit(line_surf, (x, y))
            y += self.line_height

        surf.blit(self.prompt_surf, (x, y))
        if int(t * 2) % 2 == 0:
            cursor_x = x + self.prompt_surf.get_width() + 4
            pygame.draw.rect(surf, AMIGA_CURSOR, (cursor_x, y, self.cursor_w, self.line_height - 2))

        px = self.size / 2 + math.sin(t * 0.6) * self.size * 0.4
        py = self.size / 2 + math.sin(t * 0.9 + 1.3) * self.size * 0.35
        arrow = [(px + x2 * self.scale, py + y2 * self.scale) for x2, y2 in self.ARROW_POINTS]
        pygame.draw.polygon(surf, AMIGA_POINTER, arrow)
        pygame.draw.polygon(surf, AMIGA_POINTER_DARK, arrow, 1)

        return surf

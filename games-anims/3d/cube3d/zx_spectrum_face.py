import pygame

from .colors import ZX_BLACK, ZX_BLUE, ZX_WHITE
from .face import Face
from .font_utils import fit_font
from .paths import ZX_FONT_PATH


class ZXSpectrumFace(Face):
    """ZX Spectrum 128 startup menu: a bordered box with 'Tape Loader',
    '128 BASIC', 'Calculator' and '48 BASIC', a moving selection bar,
    and the Amstrad copyright notice at the very bottom of the screen."""

    HEADER = "128"
    MENU_ITEMS = ["Tape Loader", "128 BASIC", "Calculator", "48 BASIC", ""]
    COPYRIGHT_LINES = ["(c)1985, (c)1982 Amstrad", "Consumer Electronics plc"]

    def __init__(self, size):
        super().__init__(size, ZX_WHITE)
        self.pad = max(4, int(size * 0.025))

        box_width = int(size * 0.33)
        inner_width = box_width - 2 * self.pad
        self.menu_font = fit_font(ZX_FONT_PATH, self.MENU_ITEMS + [self.HEADER], inner_width,
                                   start_size=size // 10)
        self.line_height = self.menu_font.get_linesize()

        # Size the box snugly around its content (top pad, header row, gap,
        # one row per menu item, bottom pad) so it doesn't leave extra blank
        # rows beyond the single intentional empty MENU_ITEMS entry.
        box_height = 3 * self.pad + (1 + len(self.MENU_ITEMS)) * self.line_height
        self.box_rect = pygame.Rect(0, 0, box_width, box_height)
        self.box_rect.centerx = size // 2
        self.box_rect.centery = int(size * 0.42)

        copy_width = size - 2 * self.pad
        self.copy_font = fit_font(ZX_FONT_PATH, self.COPYRIGHT_LINES, copy_width,
                                   start_size=size // 16)
        self.copy_line_height = self.copy_font.get_linesize()

    def render(self, t):
        surf = super().render(t)

        pygame.draw.rect(surf, ZX_BLACK, self.box_rect, width=2)

        header_surf = self.menu_font.render(self.HEADER, True, ZX_BLACK)
        header_y = self.box_rect.top + self.pad
        surf.blit(header_surf, (self.box_rect.centerx - header_surf.get_width() // 2, header_y))

        menu_top = header_y + self.line_height + self.pad
        selected = int(t / 1.2) % 4  # cycle through the 4 real options, forever "browsing" the menu

        for i, item in enumerate(self.MENU_ITEMS):
            y = menu_top + i * self.line_height
            row_rect = pygame.Rect(self.box_rect.left + self.pad, y,
                                    self.box_rect.width - 2 * self.pad, self.line_height)
            if item and i == selected:
                pygame.draw.rect(surf, ZX_BLUE, row_rect)
                text_color = ZX_WHITE
            else:
                text_color = ZX_BLACK
            if item:
                item_surf = self.menu_font.render(item, True, text_color)
                surf.blit(item_surf, (row_rect.left, y))

        for i, line in enumerate(self.COPYRIGHT_LINES):
            line_surf = self.copy_font.render(line, True, ZX_BLACK)
            x = self.size // 2 - line_surf.get_width() // 2
            y = self.size - self.pad - (len(self.COPYRIGHT_LINES) - i) * self.copy_line_height
            surf.blit(line_surf, (x, y))

        return surf

import pygame

from libs.colors import ZX_BLACK, ZX_WHITE, ZX_CYAN, ZX_RED, ZX_YELLOW, ZX_GREEN
from .face import Face
from libs.font_utils import fit_font
from libs.globals import ZX_FONT_PATH


class ZXSpectrumFace(Face):
    HEADER = "128"
    MENU_ITEMS = ["Tape Loader", "128 BASIC", "Calculator", "48 BASIC", ""]
    COPYRIGHT_LINES = ["(c)1985, (c)1982 Amstrad", "Consumer Electronics plc"]

    def __init__(self, size):
        super().__init__(size, ZX_WHITE)
        self.pad = max(4, int(size * 0.025))

        box_width = int(size * 0.55)
        inner_width = box_width - 2 * self.pad
        self.menu_font = fit_font(ZX_FONT_PATH, self.MENU_ITEMS + [self.HEADER], inner_width,
                                   start_size=size // 10)
        self.line_height = self.menu_font.get_linesize()

        # Size the box snugly around its content (top pad, header row,
        # one row per menu item, bottom pad) so it doesn't leave extra blank
        # rows beyond the single intentional empty MENU_ITEMS entry.
        box_height = 2 * self.pad + (1 + len(self.MENU_ITEMS)) * self.line_height
        self.box_rect = pygame.Rect(0, 0, box_width, box_height)
        self.box_rect.centerx = size // 2
        self.box_rect.centery = int(size * 0.42)

        copy_width = size - 2 * self.pad
        self.copy_font = fit_font(ZX_FONT_PATH, self.COPYRIGHT_LINES, copy_width,
                                   start_size=size // 16)
        self.copy_line_height = self.copy_font.get_linesize()

    def render(self, t):
        surf = super().render(t)
        self.draw_menu(surf, t)
        self.draw_footer(surf)
        return surf

    def draw_menu(self, surf, t):
        pygame.draw.rect(surf, ZX_BLACK, self.box_rect, width=1)
        header_y = self.box_rect.top + self.pad
        header_row = pygame.Rect(self.box_rect.left + self.pad, header_y,
                                  self.box_rect.width - 2 * self.pad, self.line_height)
        self.draw_header(surf, header_row)
        self.draw_items(surf, t, header_y + self.line_height)

    def draw_header(self, surf, header_row):
        pygame.draw.rect(surf, ZX_BLACK, header_row)
        header_surf = self.menu_font.render(self.HEADER, True, ZX_WHITE)
        surf.blit(header_surf, (header_row.left, header_row.top))
        stripes_left = header_row.left + header_surf.get_width() + self.pad
        self.draw_header_stripes(surf, header_row, stripes_left)

    def draw_header_stripes(self, surf, header_row, stripes_left):
        stripe_colors = (ZX_RED, ZX_YELLOW, ZX_GREEN, ZX_CYAN)
        slant = header_row.height
        stripe_width = (header_row.right - stripes_left) / len(stripe_colors) * 0.25
        stripes_start = header_row.right - stripe_width * len(stripe_colors) - 10
        top, bottom = header_row.top, header_row.bottom

        previous_clip = surf.get_clip()
        surf.set_clip(header_row)
        for index, color in enumerate(stripe_colors):
            left = stripes_start + index * stripe_width
            right = left + stripe_width
            trapeze = [(left, bottom), (left + slant, top),
                       (right + slant, top), (right, bottom)]
            pygame.draw.polygon(surf, color, trapeze)
        surf.set_clip(previous_clip)

    def draw_items(self, surf, t, menu_top):
        selected = int(t / 1.2) % 4  # cycle through the 4 real options, forever "browsing" the menu
        for index, item in enumerate(self.MENU_ITEMS):
            if not item:
                continue
            y = menu_top + index * self.line_height
            row_rect = pygame.Rect(self.box_rect.left + self.pad, y,
                                    self.box_rect.width - 2 * self.pad, self.line_height)
            if index == selected:
                pygame.draw.rect(surf, ZX_CYAN, row_rect)
            item_surf = self.menu_font.render(item, True, ZX_BLACK)
            surf.blit(item_surf, (row_rect.left, y))

    def draw_footer(self, surf):
        for i, line in enumerate(self.COPYRIGHT_LINES):
            line_surf = self.copy_font.render(line, True, ZX_BLACK)
            x = self.size // 2 - line_surf.get_width() // 2
            y = self.size - self.pad - (len(self.COPYRIGHT_LINES) - i) * self.copy_line_height
            surf.blit(line_surf, (x, y))

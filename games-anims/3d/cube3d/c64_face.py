import pygame

from .colors import C64_DARK_BLUE, C64_LIGHT_BLUE, C64_TEXT_COLOR
from .face import Face
from .font_utils import fit_font_size
from .globals import C64_FONT_PATH


class C64Face(Face):
    LINES = [
        "**** COMMODORE 64 BASIC V2 ****",
        "",
        " 64K RAM SYSTEM  38911 BASIC BYTES FREE ",
        "",
        "READY.",
    ]

    def __init__(self, size):
        super().__init__(size, C64_LIGHT_BLUE)
        self.margin = int(size * 0.08)
        self.inner_pad = max(4, int(size * 0.025))

        content_width = size - 2 * self.margin - 2 * self.inner_pad
        fitted_size = fit_font_size(C64_FONT_PATH, self.LINES, content_width, start_size=size // 15)

        self.font = pygame.font.Font(C64_FONT_PATH, fitted_size + 1)
        self.line_height = self.font.get_linesize()
        self.cursor_w = self.font.size("@")[0]

    def render(self, t):
        surf = super().render(t)

        screen_rect = pygame.Rect(self.margin, self.margin,
                                   self.size - 2 * self.margin, self.size - 2 * self.margin)
        pygame.draw.rect(surf, C64_DARK_BLUE, screen_rect)

        rendered = [self.font.render(line, True, C64_TEXT_COLOR) for line in self.LINES]
        start_y = screen_rect.top + self.inner_pad
        left_x = screen_rect.left

        for i, (line, text_surf) in enumerate(zip(self.LINES, rendered)):
            if line == "READY.":
                x = left_x
            else:
                x = screen_rect.centerx - text_surf.get_width() // 2
            y = start_y + i * self.line_height
            surf.blit(text_surf, (x, y))

        cursor_y = start_y + len(rendered) * self.line_height

        if int(t * 2) % 2 == 0:
            pygame.draw.rect(
                surf, C64_TEXT_COLOR,
                (left_x, cursor_y, self.cursor_w, self.line_height)
            )

        return surf
